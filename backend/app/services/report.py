from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    User, StudentProfile,
    ReportPeriod, PeriodType, ReportStatus,
    ReportEntry,
    Comment, EntityType
)
from app.schemas.report import (
    ReportPeriodCreate, ReportEntryCreate, ReportEntryUpdate,
    QuickUpdate, TimeAllocation
)


class ReportService:
    
    @staticmethod
    async def get_or_create_current_period(
        db: AsyncSession,
        student_id: int
    ) -> ReportPeriod:
        """Get current report period or create if doesn't exist"""
        # Get student profile to check start date
        result = await db.execute(
            select(StudentProfile).where(StudentProfile.user_id == student_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            raise ValueError(f"Student profile not found for user {student_id}")
        
        # Find current period
        today = date.today()
        result = await db.execute(
            select(ReportPeriod).where(
                and_(
                    ReportPeriod.student_id == student_id,
                    ReportPeriod.start_date <= today,
                    ReportPeriod.end_date >= today
                )
            )
        )
        current_period = result.scalar_one_or_none()
        
        if current_period:
            return current_period
        
        # Create new period if none exists
        # Calculate period dates (bi-weekly from start date)
        days_since_start = (today - profile.start_date).days
        period_number = days_since_start // 14
        
        start_date = profile.start_date + timedelta(days=period_number * 14)
        end_date = start_date + timedelta(days=13)
        due_date = end_date + timedelta(days=3)  # 3 days after period ends
        
        new_period = ReportPeriod(
            student_id=student_id,
            period_type=PeriodType.BIWEEKLY,
            start_date=start_date,
            end_date=end_date,
            due_date=due_date,
            status=ReportStatus.PENDING
        )
        db.add(new_period)
        await db.commit()
        await db.refresh(new_period)
        
        return new_period
    
    @staticmethod
    async def get_report_periods(
        db: AsyncSession,
        student_id: int,
        status: Optional[ReportStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[ReportPeriod]:
        """Get report periods for a student"""
        query = select(ReportPeriod).where(
            ReportPeriod.student_id == student_id
        )
        
        if status:
            query = query.where(ReportPeriod.status == status)
        
        query = query.order_by(desc(ReportPeriod.start_date)).limit(limit).offset(offset)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_previous_report(
        db: AsyncSession,
        student_id: int,
        before_date: date
    ) -> Optional[ReportEntry]:
        """Get the most recent submitted report before a given date"""
        result = await db.execute(
            select(ReportEntry)
            .join(ReportPeriod)
            .where(
                and_(
                    ReportEntry.student_id == student_id,
                    ReportPeriod.end_date < before_date,
                    ReportPeriod.status == ReportStatus.SUBMITTED
                )
            )
            .order_by(desc(ReportPeriod.end_date))
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def auto_populate_from_previous(
        db: AsyncSession,
        student_id: int,
        current_period: ReportPeriod
    ) -> Dict[str, Any]:
        """Auto-populate fields from previous report"""
        previous = await ReportService.get_previous_report(
            db, student_id, current_period.start_date
        )
        
        if not previous:
            return {}
        
        # Parse previous next_period_plan into accomplishments
        auto_populated = {
            "accomplishments": f"From previous period plan:\n{previous.next_period_plan}",
            "time_allocation": previous.time_allocation,
            "tags": previous.tags
        }
        
        return auto_populated
    
    @staticmethod
    async def submit_report(
        db: AsyncSession,
        student_id: int,
        report_data: ReportEntryCreate
    ) -> ReportEntry:
        """Submit or update a report"""
        # Check if report already exists
        result = await db.execute(
            select(ReportEntry).where(
                and_(
                    ReportEntry.period_id == report_data.period_id,
                    ReportEntry.student_id == student_id
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing report
            for field, value in report_data.dict(exclude_unset=True).items():
                if field == "time_allocation":
                    # value is already a dict from Pydantic
                    setattr(existing, field, value)
                elif field != "is_draft":  # Skip is_draft field
                    setattr(existing, field, value)
            existing.version += 1
            report = existing
        else:
            # Create new report
            report_dict = report_data.dict(exclude={"is_draft"})  # Exclude is_draft
            report_dict["time_allocation"] = report_data.time_allocation.dict()
            report = ReportEntry(
                student_id=student_id,
                **report_dict
            )
            db.add(report)
        
        # Update period status if not a draft
        if not report_data.is_draft:
            period = await db.get(ReportPeriod, report_data.period_id)
            if period:
                period.status = ReportStatus.SUBMITTED
        
        await db.commit()
        await db.refresh(report)
        return report
    
    @staticmethod
    async def quick_update_report(
        db: AsyncSession,
        report_id: int,
        student_id: int,
        update_data: QuickUpdate
    ) -> ReportEntry:
        """Submit a quick update for current period"""
        # Get current period
        current_period = await ReportService.get_or_create_current_period(db, student_id)
        
        # Create minimal report
        quick_messages = {
            "steady_progress": "Steady progress on all fronts. Research and writing proceeding as planned.",
            "focus_week": "Deep focus week on research/writing. Limited meetings and other activities.",
            "blocked": "Encountered blockers this period. See notes for details."
        }
        
        report_data = ReportEntryCreate(
            period_id=current_period.id,
            accomplishments=quick_messages[update_data.status],
            blockers=update_data.note if update_data.status == "blocked" else None,
            next_period_plan="Continue current work",
            time_allocation=TimeAllocation(
                research=60,
                writing=30,
                meetings=10,
                teaching=0,
                other=0
            ),
            is_draft=False
        )
        
        if update_data.note and update_data.status != "blocked":
            report_data.accomplishments += f"\n\nNote: {update_data.note}"
        
        return await ReportService.submit_report(db, student_id, report_data)
    
    @staticmethod
    async def get_report_by_id(
        db: AsyncSession,
        report_id: int
    ) -> Optional[ReportEntry]:
        """Get report by ID with period info"""
        result = await db.execute(
            select(ReportEntry)
            .options(selectinload(ReportEntry.report_period))
            .where(ReportEntry.id == report_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def add_comment_to_report(
        db: AsyncSession,
        report_id: int,
        author_id: int,
        content: str,
        visibility: str = "public"
    ) -> Comment:
        """Add a comment to a report"""
        comment = Comment(
            entity_type=EntityType.REPORT,
            entity_id=report_id,
            author_id=author_id,
            content=content,
            visibility=visibility
        )
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    
    @staticmethod
    async def acknowledge_report(
        db: AsyncSession,
        report_id: int,
        supervisor_id: int,
        comment: Optional[str] = None
    ) -> bool:
        """Supervisor acknowledges a report"""
        # Verify the supervisor has access to this report
        result = await db.execute(
            select(ReportEntry)
            .join(StudentProfile, StudentProfile.user_id == ReportEntry.student_id)
            .where(
                and_(
                    ReportEntry.id == report_id,
                    or_(
                        StudentProfile.supervisor_id == supervisor_id,
                        StudentProfile.co_supervisor_id == supervisor_id
                    )
                )
            )
        )
        report = result.scalar_one_or_none()
        
        if not report:
            return False
        
        # Add acknowledgment comment
        if comment:
            await ReportService.add_comment_to_report(
                db, report_id, supervisor_id,
                f"Acknowledged. {comment}",
                "supervisor_only"
            )
        else:
            await ReportService.add_comment_to_report(
                db, report_id, supervisor_id,
                "Report acknowledged.",
                "supervisor_only"
            )
        
        return True
    
    @staticmethod
    async def get_student_reports_for_supervisor(
        db: AsyncSession,
        supervisor_id: int,
        status: Optional[ReportStatus] = None
    ) -> List[Dict[str, Any]]:
        """Get all reports for students supervised by this supervisor"""
        query = select(
            ReportEntry,
            ReportPeriod,
            User
        ).join(
            ReportPeriod, ReportEntry.period_id == ReportPeriod.id
        ).join(
            User, ReportEntry.student_id == User.id
        ).join(
            StudentProfile, StudentProfile.user_id == User.id
        ).where(
            or_(
                StudentProfile.supervisor_id == supervisor_id,
                StudentProfile.co_supervisor_id == supervisor_id
            )
        )
        
        if status:
            query = query.where(ReportPeriod.status == status)
        
        query = query.order_by(desc(ReportPeriod.due_date))
        
        result = await db.execute(query)
        reports = []
        
        for entry, period, user in result:
            reports.append({
                "report": entry,
                "period": period,
                "student": user
            })
        
        return reports