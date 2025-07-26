"""Notification service for managing notifications."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import logging

from app.models.user import User
from app.models.notification_preference import NotificationPreference
from app.models.notification_log import NotificationLog, NotificationType, NotificationChannel, NotificationStatus
from app.models.reminder_schedule import ReminderSchedule, ReminderEntityType
from app.models.report_period import ReportPeriod
from app.services.email_service import email_service

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for handling notifications and reminders."""
    
    @staticmethod
    async def create_in_app_notification(
        db: AsyncSession,
        user_id: int,
        type: NotificationType,
        subject: str,
        content: str,
        extra_data: Dict[str, Any] = None
    ) -> NotificationLog:
        """Create an in-app notification."""
        notification = NotificationLog(
            user_id=user_id,
            type=type,
            channel=NotificationChannel.IN_APP,
            subject=subject,
            content=content,
            status=NotificationStatus.SENT,
            sent_at=datetime.utcnow(),
            extra_data=extra_data or {}
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification
    
    @staticmethod
    async def schedule_report_reminders(
        db: AsyncSession,
        report_period: ReportPeriod,
        student_id: int
    ) -> List[ReminderSchedule]:
        """Schedule reminders for a report period."""
        reminders = []
        
        # Define reminder schedule
        reminder_schedule = [
            ("T-3days", timedelta(days=-3), False),  # 3 days before
            ("T-0", timedelta(days=0), False),       # Due date
            ("T+2days", timedelta(days=2), False),   # 2 days after
            ("T+7days", timedelta(days=7), True),    # 7 days after (notify supervisor)
        ]
        
        for reminder_type, delta, include_supervisor in reminder_schedule:
            scheduled_date = report_period.end_date + delta
            
            # Skip if scheduled date is in the past
            if scheduled_date.date() < datetime.utcnow().date():
                continue
            
            # Create reminder
            reminder = ReminderSchedule(
                entity_type=ReminderEntityType.REPORT_PERIOD,
                entity_id=report_period.id,
                scheduled_for=datetime.combine(scheduled_date, datetime.min.time().replace(hour=9)),
                reminder_type=reminder_type,
                user_id=student_id,
                include_supervisor=include_supervisor
            )
            db.add(reminder)
            reminders.append(reminder)
        
        await db.commit()
        return reminders
    
    @staticmethod
    async def process_reminder(
        db: AsyncSession,
        reminder: ReminderSchedule
    ) -> bool:
        """Process a single reminder."""
        try:
            # Get user
            user_stmt = select(User).where(User.id == reminder.user_id)
            user = await db.scalar(user_stmt)
            
            if not user:
                logger.error(f"User {reminder.user_id} not found for reminder {reminder.id}")
                return False
            
            # Get user preferences
            prefs_stmt = select(NotificationPreference).where(
                NotificationPreference.user_id == user.id
            )
            prefs = await db.scalar(prefs_stmt)
            
            # Get entity details based on type
            entity_details = {}
            if reminder.entity_type == ReminderEntityType.REPORT_PERIOD:
                period_stmt = select(ReportPeriod).where(ReportPeriod.id == reminder.entity_id)
                period = await db.scalar(period_stmt)
                if period:
                    entity_details = {
                        'title': f'{period.period_type.value.capitalize()} Report',
                        'due_date': period.end_date.strftime('%B %d, %Y')
                    }
            
            # Send notifications through enabled channels
            success = False
            
            # Email notification
            if not prefs or prefs.email_enabled:
                email_sent = await email_service.send_reminder_email(
                    to_email=user.email,
                    user_name=user.full_name,
                    reminder_type=reminder.reminder_type,
                    entity_type=reminder.entity_type.value,
                    entity_details=entity_details
                )
                
                if email_sent:
                    # Log email notification
                    email_log = NotificationLog(
                        user_id=user.id,
                        type=NotificationType.REMINDER,
                        channel=NotificationChannel.EMAIL,
                        subject=f"Reminder: {entity_details.get('title', 'Deadline')}",
                        content=f"Reminder sent for {reminder.reminder_type}",
                        sent_at=datetime.utcnow(),
                        status=NotificationStatus.SENT,
                        extra_data={'reminder_id': reminder.id}
                    )
                    db.add(email_log)
                    success = True
            
            # In-app notification
            await NotificationService.create_in_app_notification(
                db=db,
                user_id=user.id,
                type=NotificationType.REMINDER,
                subject=f"Reminder: {entity_details.get('title', 'Deadline')}",
                content=f"Your {entity_details.get('title', 'deadline')} is due on {entity_details.get('due_date', 'soon')}",
                extra_data={'reminder_id': reminder.id, 'entity_type': reminder.entity_type.value}
            )
            
            # Mark reminder as processed
            reminder.processed = True
            reminder.processed_at = datetime.utcnow()
            
            await db.commit()
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing reminder {reminder.id}: {str(e)}")
            await db.rollback()
            return False
    
    @staticmethod
    async def process_due_reminders(db: AsyncSession) -> int:
        """Process all due reminders."""
        # Get unprocessed reminders due now or in the past
        stmt = select(ReminderSchedule).where(
            and_(
                ReminderSchedule.processed == False,
                ReminderSchedule.scheduled_for <= datetime.utcnow()
            )
        )
        
        result = await db.execute(stmt)
        reminders = result.scalars().all()
        
        processed_count = 0
        for reminder in reminders:
            if await NotificationService.process_reminder(db, reminder):
                processed_count += 1
        
        return processed_count