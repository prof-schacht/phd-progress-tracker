"""Notification API endpoints."""

from typing import Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.notification_preference import NotificationPreference
from app.models.notification_log import NotificationLog, NotificationChannel, NotificationStatus, NotificationType
from app.schemas.notification import (
    NotificationPreference as NotificationPreferenceSchema,
    NotificationPreferenceCreate,
    NotificationPreferenceUpdate,
    InAppNotification,
    InAppNotificationList,
    TestNotificationRequest
)
from app.services.email_service import email_service
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("/preferences", response_model=NotificationPreferenceSchema)
async def get_notification_preferences(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user's notification preferences."""
    # Try to get existing preferences
    stmt = select(NotificationPreference).where(
        NotificationPreference.user_id == current_user.id
    )
    prefs = await db.scalar(stmt)
    
    # Create default preferences if none exist
    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)
        await db.commit()
        await db.refresh(prefs)
    
    return prefs


@router.put("/preferences", response_model=NotificationPreferenceSchema)
async def update_notification_preferences(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    preferences: NotificationPreferenceUpdate
) -> Any:
    """Update notification preferences."""
    # Get existing preferences
    stmt = select(NotificationPreference).where(
        NotificationPreference.user_id == current_user.id
    )
    prefs = await db.scalar(stmt)
    
    if not prefs:
        # Create with updates
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)
    
    # Update fields
    update_data = preferences.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prefs, field, value)
    
    await db.commit()
    await db.refresh(prefs)
    
    return prefs


@router.get("", response_model=InAppNotificationList)
async def get_notifications(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = False
) -> Any:
    """Get user's in-app notifications."""
    # Base query
    query = select(NotificationLog).where(
        and_(
            NotificationLog.user_id == current_user.id,
            NotificationLog.channel == NotificationChannel.IN_APP
        )
    )
    
    if unread_only:
        query = query.where(NotificationLog.read_at.is_(None))
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Get unread count
    unread_query = select(func.count()).select_from(
        select(NotificationLog).where(
            and_(
                NotificationLog.user_id == current_user.id,
                NotificationLog.channel == NotificationChannel.IN_APP,
                NotificationLog.read_at.is_(None)
            )
        ).subquery()
    )
    unread_count = await db.scalar(unread_query)
    
    # Get items
    query = query.order_by(NotificationLog.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    # Convert to InAppNotification schema
    items = []
    for notif in notifications:
        items.append(InAppNotification(
            id=notif.id,
            type=notif.type,
            subject=notif.subject,
            content=notif.content,
            created_at=notif.created_at,
            read_at=notif.read_at,
            extra_data=notif.extra_data
        ))
    
    return InAppNotificationList(
        items=items,
        total=total,
        unread_count=unread_count
    )


@router.put("/{notification_id}/read")
async def mark_notification_read(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    notification_id: int
) -> Any:
    """Mark a notification as read."""
    # Get notification
    stmt = select(NotificationLog).where(
        and_(
            NotificationLog.id == notification_id,
            NotificationLog.user_id == current_user.id,
            NotificationLog.channel == NotificationChannel.IN_APP
        )
    )
    notification = await db.scalar(stmt)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if not notification.read_at:
        notification.read_at = datetime.utcnow()
        await db.commit()
    
    return {"message": "Notification marked as read"}


@router.post("/test")
async def send_test_notification(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: TestNotificationRequest
) -> Any:
    """Send a test notification to verify settings."""
    # Determine email
    email = request.email or current_user.email
    
    # Send test email
    success = await email_service.send_test_email(email)
    
    if success:
        # Log the notification
        notification_log = NotificationLog(
            user_id=current_user.id,
            type=NotificationType.ANNOUNCEMENT,
            channel=NotificationChannel.EMAIL,
            subject="PhD Progress Tracker - Test Email",
            content="Test email sent to verify configuration",
            sent_at=datetime.utcnow(),
            status=NotificationStatus.SENT
        )
        db.add(notification_log)
        await db.commit()
        
        return {"message": f"Test email sent to {email}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test email"
        )