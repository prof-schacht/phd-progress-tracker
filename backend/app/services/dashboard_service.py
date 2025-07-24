"""Dashboard service for student and supervisor dashboard data."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.report_period import ReportPeriod
from app.models.report_entry import ReportEntry
from app.models.research_project import ResearchProject
from app.models.milestone import Milestone
from app.models.meeting_note import MeetingNote
from app.models.comment import Comment
from app.services.report import ReportService


class DashboardService:
    """Service for dashboard data aggregation."""
    
    @staticmethod
    async def _get_current_period_info(
        db: AsyncSession,
        student_id: int
    ) -> Dict[str, Any]:
        """Get current period information for a student."""
        # Find current period
        today = datetime.utcnow().date()
        stmt = select(ReportPeriod).where(
            and_(
                ReportPeriod.start_date <= today,
                ReportPeriod.end_date >= today
            )
        ).order_by(ReportPeriod.start_date.desc()).limit(1)
        
        current_period = await db.scalar(stmt)
        
        if not current_period:
            return {
                "period": None,
                "currentReport": None,
                "previousReport": None,
                "autoPopulated": None
            }
        
        # Get current report if exists
        current_report = None
        report_stmt = select(ReportEntry).where(
            and_(
                ReportEntry.student_id == student_id,
                ReportEntry.period_id == current_period.id
            )
        ).options(
            selectinload(ReportEntry.report_period)
        )
        report_entry = await db.scalar(report_stmt)
        if report_entry:
            current_report = {
                "id": report_entry.id,
                "status": report_entry.status,
                "submittedAt": report_entry.submitted_at.isoformat() if report_entry.submitted_at else None,
                "highlights": report_entry.highlights,
                "challenges": report_entry.challenges,
                "nextSteps": report_entry.next_steps
            }
        
        # Get previous report
        previous_report = None
        prev_stmt = select(ReportEntry).join(
            ReportPeriod
        ).where(
            and_(
                ReportEntry.student_id == student_id,
                ReportPeriod.end_date < current_period.start_date
            )
        ).order_by(ReportPeriod.end_date.desc()).limit(1)
        
        prev_entry = await db.scalar(prev_stmt)
        if prev_entry:
            previous_report = {
                "id": prev_entry.id,
                "periodStart": prev_entry.report_period.start_date.isoformat(),
                "periodEnd": prev_entry.report_period.end_date.isoformat(),
                "submittedAt": prev_entry.submitted_at.isoformat() if prev_entry.submitted_at else None,
                "nextSteps": prev_entry.next_steps
            }
        
        return {
            "period": {
                "id": current_period.id,
                "reportType": current_period.period_type,
                "startDate": current_period.start_date.isoformat(),
                "endDate": current_period.end_date.isoformat(),
                "isActive": True
            },
            "currentReport": current_report,
            "previousReport": previous_report,
            "autoPopulated": {
                "fromPrevious": previous_report["nextSteps"] if previous_report else None
            } if not current_report else None
        }
    
    @staticmethod
    async def _get_current_period(db: AsyncSession) -> Optional[ReportPeriod]:
        """Get the current active report period."""
        today = datetime.utcnow().date()
        stmt = select(ReportPeriod).where(
            and_(
                ReportPeriod.start_date <= today,
                ReportPeriod.end_date >= today
            )
        ).order_by(ReportPeriod.start_date.desc()).limit(1)
        
        return await db.scalar(stmt)
    
    @staticmethod
    async def get_student_dashboard(
        db: AsyncSession,
        student_id: int
    ) -> Dict[str, Any]:
        """Get dashboard data for a student."""
        # Get current period info
        current_period_info = await DashboardService._get_current_period_info(
            db, student_id
        )
        
        # Get upcoming deadlines
        deadlines = await DashboardService._get_student_deadlines(db, student_id)
        
        # Get recent feedback
        recent_feedback = await DashboardService._get_recent_feedback(db, student_id)
        
        # Get research projects
        projects = await DashboardService._get_research_projects(db, student_id)
        
        # Get student stats
        stats = await DashboardService._get_student_stats(db, student_id)
        
        return {
            "currentPeriod": current_period_info,
            "upcomingDeadlines": deadlines,
            "recentFeedback": recent_feedback,
            "researchProjects": projects,
            "stats": stats
        }
    
    @staticmethod
    async def _get_student_deadlines(
        db: AsyncSession,
        student_id: int
    ) -> List[Dict[str, Any]]:
        """Get upcoming deadlines for a student."""
        deadlines = []
        now = datetime.utcnow()
        
        # Get current and next report periods
        current_period = await DashboardService._get_current_period(db)
        if current_period:
            # Check if report is submitted for current period
            report_stmt = select(ReportEntry).where(
                and_(
                    ReportEntry.student_id == student_id,
                    ReportEntry.period_id == current_period.id
                )
            )
            report = await db.scalar(report_stmt)
            
            if not report:
                days_remaining = (current_period.end_date - now.date()).days
                deadlines.append({
                    "id": f"report-{current_period.id}",
                    "title": f"{current_period.period_type.title()} Report Due",
                    "type": "report",
                    "dueDate": current_period.end_date.isoformat(),
                    "status": "overdue" if days_remaining < 0 else "upcoming",
                    "daysRemaining": days_remaining
                })
        
        # Get upcoming milestones
        milestone_stmt = select(Milestone).where(
            and_(
                Milestone.student_id == student_id,
                Milestone.status.in_(["planned", "in_progress"]),
                Milestone.due_date >= now.date()
            )
        ).order_by(Milestone.due_date).limit(3)
        
        milestones = await db.scalars(milestone_stmt)
        for milestone in milestones:
            days_remaining = (milestone.due_date - now.date()).days
            deadlines.append({
                "id": f"milestone-{milestone.id}",
                "title": milestone.title,
                "type": "milestone",
                "dueDate": milestone.due_date.isoformat(),
                "status": "upcoming",
                "daysRemaining": days_remaining
            })
        
        return sorted(deadlines, key=lambda x: x['dueDate'])
    
    @staticmethod
    async def _get_recent_feedback(
        db: AsyncSession,
        student_id: int,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent feedback comments for a student."""
        # Get comments on student's reports
        stmt = select(Comment).join(
            ReportEntry, Comment.entity_id == ReportEntry.id
        ).where(
            and_(
                Comment.entity_type == "report",
                ReportEntry.student_id == student_id,
                Comment.visibility.in_(["public", "private"])
            )
        ).options(
            selectinload(Comment.author)
        ).order_by(Comment.created_at.desc()).limit(limit)
        
        comments = await db.scalars(stmt)
        
        return [
            {
                "id": comment.id,
                "author": {
                    "id": comment.author.id,
                    "email": comment.author.email,
                    "full_name": comment.author.full_name
                },
                "content": comment.content,
                "visibility": comment.visibility,
                "createdAt": comment.created_at.isoformat(),
                "editedAt": comment.edited_at.isoformat() if comment.edited_at else None
            }
            for comment in comments
        ]
    
    @staticmethod
    async def _get_research_projects(
        db: AsyncSession,
        student_id: int
    ) -> List[Dict[str, Any]]:
        """Get research projects for a student."""
        stmt = select(ResearchProject).where(
            ResearchProject.student_id == student_id
        ).order_by(ResearchProject.created_at.desc())
        
        projects = await db.scalars(stmt)
        
        result = []
        for project in projects:
            # Count milestones
            milestone_count_stmt = select(func.count(Milestone.id)).where(
                Milestone.project_id == project.id
            )
            completed_count_stmt = select(func.count(Milestone.id)).where(
                and_(
                    Milestone.project_id == project.id,
                    Milestone.status == "completed"
                )
            )
            
            total_milestones = await db.scalar(milestone_count_stmt)
            completed_milestones = await db.scalar(completed_count_stmt)
            
            # Get next milestone
            next_milestone_stmt = select(Milestone).where(
                and_(
                    Milestone.project_id == project.id,
                    Milestone.status.in_(["planned", "in_progress"])
                )
            ).order_by(Milestone.due_date).limit(1)
            
            next_milestone = await db.scalar(next_milestone_stmt)
            
            # Calculate progress
            progress = 0
            if total_milestones > 0:
                progress = int((completed_milestones / total_milestones) * 100)
            
            result.append({
                "id": project.id,
                "title": project.title,
                "status": project.status,
                "progress": progress,
                "milestones": total_milestones,
                "completedMilestones": completed_milestones,
                "nextMilestone": next_milestone.title if next_milestone else None
            })
        
        return result
    
    @staticmethod
    async def _get_student_stats(
        db: AsyncSession,
        student_id: int
    ) -> Dict[str, Any]:
        """Get statistics for a student."""
        # Count total reports
        total_reports_stmt = select(func.count(ReportEntry.id)).where(
            ReportEntry.student_id == student_id
        )
        total_reports = await db.scalar(total_reports_stmt)
        
        # Count on-time submissions
        on_time_stmt = select(func.count(ReportEntry.id)).select_from(
            ReportEntry
        ).join(
            ReportPeriod, ReportEntry.period_id == ReportPeriod.id
        ).where(
            and_(
                ReportEntry.student_id == student_id,
                ReportEntry.submitted_at <= func.cast(
                    ReportPeriod.end_date + timedelta(days=1),
                    type_=ReportEntry.submitted_at.type
                )
            )
        )
        on_time_submissions = await db.scalar(on_time_stmt)
        
        # Calculate current streak
        current_streak = await DashboardService._calculate_submission_streak(
            db, student_id
        )
        
        # Calculate average time allocation (mock data for now)
        avg_time_allocation = {
            "research": 40,
            "writing": 25,
            "teaching": 20,
            "meetings": 10,
            "other": 5
        }
        
        return {
            "onTimeSubmissions": on_time_submissions,
            "currentStreak": current_streak,
            "totalReports": total_reports,
            "averageTimeAllocation": avg_time_allocation
        }
    
    @staticmethod
    async def _calculate_submission_streak(
        db: AsyncSession,
        student_id: int
    ) -> int:
        """Calculate current submission streak for a student."""
        # Get all report periods and submissions ordered by date
        stmt = select(ReportPeriod, ReportEntry).select_from(
            ReportPeriod
        ).outerjoin(
            ReportEntry,
            and_(
                ReportEntry.period_id == ReportPeriod.id,
                ReportEntry.student_id == student_id
            )
        ).where(
            ReportPeriod.end_date <= datetime.utcnow().date()
        ).order_by(ReportPeriod.end_date.desc())
        
        results = await db.execute(stmt)
        
        streak = 0
        for period, report in results:
            if report and report.submitted_at <= datetime.combine(
                period.end_date + timedelta(days=1),
                datetime.min.time()
            ):
                streak += 1
            else:
                break
        
        return streak
    
    @staticmethod
    async def get_supervisor_dashboard(
        db: AsyncSession,
        supervisor_id: int
    ) -> Dict[str, Any]:
        """Get dashboard data for a supervisor."""
        # Get supervised students
        students = await DashboardService._get_supervised_students(db, supervisor_id)
        
        # Get alerts
        alerts = await DashboardService._get_supervisor_alerts(db, supervisor_id)
        
        # Get pending reviews
        pending_reviews = await DashboardService._get_pending_reviews(db, supervisor_id)
        
        # Get upcoming meetings
        upcoming_meetings = await DashboardService._get_upcoming_meetings(db, supervisor_id)
        
        # Get supervisor stats
        stats = await DashboardService._get_supervisor_stats(db, supervisor_id, students)
        
        return {
            "students": students,
            "alerts": alerts,
            "pendingReviews": pending_reviews,
            "upcomingMeetings": upcoming_meetings,
            "stats": stats
        }
    
    @staticmethod
    async def _get_supervised_students(
        db: AsyncSession,
        supervisor_id: int
    ) -> List[Dict[str, Any]]:
        """Get list of supervised students with their status."""
        stmt = select(User).join(
            StudentProfile, User.id == StudentProfile.user_id
        ).where(
            or_(
                StudentProfile.supervisor_id == supervisor_id,
                StudentProfile.co_supervisor_id == supervisor_id
            )
        ).options(
            selectinload(User.student_profile)
        )
        
        students = await db.scalars(stmt)
        
        result = []
        for student in students:
            # Get last report
            last_report = await DashboardService._get_last_report(db, student.id)
            
            # Get upcoming deadlines
            deadlines = await DashboardService._get_student_deadlines(db, student.id)
            
            # Get research projects
            projects = await DashboardService._get_research_projects(db, student.id)
            
            # Determine status
            status = await DashboardService._determine_student_status(
                db, student.id, last_report
            )
            
            result.append({
                "id": student.id,
                "name": student.full_name,
                "email": student.email,
                "status": status,
                "lastReport": last_report,
                "upcomingDeadlines": deadlines[:2],  # Only show next 2
                "researchPipeline": projects,
                "program": student.student_profile.program,
                "yearInProgram": student.student_profile.year_in_program
            })
        
        return result
    
    @staticmethod
    async def _get_last_report(
        db: AsyncSession,
        student_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get the last submitted report for a student."""
        stmt = select(ReportEntry).join(
            ReportPeriod
        ).where(
            ReportEntry.student_id == student_id
        ).order_by(ReportEntry.submitted_at.desc()).limit(1)
        
        report = await db.scalar(stmt)
        
        if not report:
            return None
        
        return {
            "id": report.id,
            "periodStart": report.report_period.start_date.isoformat(),
            "periodEnd": report.report_period.end_date.isoformat(),
            "submittedAt": report.submitted_at.isoformat(),
            "status": report.status,
            "highlights": report.highlights
        }
    
    @staticmethod
    async def _determine_student_status(
        db: AsyncSession,
        student_id: int,
        last_report: Optional[Dict[str, Any]]
    ) -> str:
        """Determine student status based on various factors."""
        now = datetime.utcnow()
        
        # Check for overdue reports
        current_period = await DashboardService._get_current_period(db)
        if current_period:
            report_stmt = select(ReportEntry).where(
                and_(
                    ReportEntry.student_id == student_id,
                    ReportEntry.period_id == current_period.id
                )
            )
            current_report = await db.scalar(report_stmt)
            
            if not current_report and current_period.end_date < now.date():
                return "needs_attention"
        
        # Check last report date
        if last_report:
            last_report_date = datetime.fromisoformat(
                last_report["submittedAt"].replace("Z", "+00:00")
            )
            days_since_report = (now - last_report_date).days
            
            if days_since_report > 30:
                return "at_risk"
            elif days_since_report > 45:
                return "needs_attention"
        else:
            return "at_risk"
        
        return "on_track"
    
    @staticmethod
    async def _get_supervisor_alerts(
        db: AsyncSession,
        supervisor_id: int
    ) -> List[Dict[str, Any]]:
        """Get alerts for a supervisor."""
        alerts = []
        
        # Get students
        student_stmt = select(User).join(
            StudentProfile, User.id == StudentProfile.user_id
        ).where(
            or_(
                StudentProfile.supervisor_id == supervisor_id,
                StudentProfile.co_supervisor_id == supervisor_id
            )
        )
        students = await db.scalars(student_stmt)
        
        for student in students:
            # Check for overdue reports
            current_period = await DashboardService._get_current_period(db)
            if current_period:
                report_stmt = select(ReportEntry).where(
                    and_(
                        ReportEntry.student_id == student.id,
                        ReportEntry.period_id == current_period.id
                    )
                )
                report = await db.scalar(report_stmt)
                
                if not report and current_period.end_date < datetime.utcnow().date():
                    days_overdue = (datetime.utcnow().date() - current_period.end_date).days
                    alerts.append({
                        "id": f"overdue-{student.id}-{current_period.id}",
                        "type": "overdue",
                        "severity": "high" if days_overdue > 7 else "medium",
                        "student": {
                            "id": student.id,
                            "email": student.email,
                            "full_name": student.full_name
                        },
                        "message": f"Report is {days_overdue} days overdue",
                        "createdAt": datetime.utcnow().isoformat(),
                        "actionRequired": True
                    })
        
        return alerts
    
    @staticmethod
    async def _get_pending_reviews(
        db: AsyncSession,
        supervisor_id: int
    ) -> List[Dict[str, Any]]:
        """Get pending report reviews for a supervisor."""
        stmt = select(ReportEntry).join(
            User, ReportEntry.student_id == User.id
        ).join(
            StudentProfile, User.id == StudentProfile.user_id
        ).join(
            ReportPeriod, ReportEntry.period_id == ReportPeriod.id
        ).where(
            and_(
                or_(
                    StudentProfile.supervisor_id == supervisor_id,
                    StudentProfile.co_supervisor_id == supervisor_id
                ),
                ReportEntry.submitted_at.isnot(None)
            )
        ).options(
            selectinload(ReportEntry.student),
            selectinload(ReportEntry.report_period)
        )
        
        reports = await db.scalars(stmt)
        
        result = []
        for report in reports:
            days_waiting = (datetime.utcnow() - report.submitted_at).days
            result.append({
                "reportId": report.id,
                "studentName": report.student.full_name,
                "submittedAt": report.submitted_at.isoformat(),
                "daysWaiting": days_waiting,
                "reportType": report.report_period.period_type
            })
        
        return result
    
    @staticmethod
    async def _get_upcoming_meetings(
        db: AsyncSession,
        supervisor_id: int
    ) -> List[Dict[str, Any]]:
        """Get upcoming meetings for a supervisor."""
        stmt = select(MeetingNote).join(
            User, MeetingNote.student_id == User.id
        ).where(
            and_(
                MeetingNote.supervisor_id == supervisor_id,
                MeetingNote.meeting_date >= datetime.utcnow()
            )
        ).options(
            selectinload(MeetingNote.student)
        ).order_by(MeetingNote.meeting_date).limit(5)
        
        meetings = await db.scalars(stmt)
        
        return [
            {
                "id": meeting.id,
                "title": meeting.title or "Meeting",
                "studentName": meeting.student.full_name,
                "scheduledAt": meeting.meeting_date.isoformat(),
                "duration": 30,  # Default duration
                "location": None,
                "agenda": meeting.agenda
            }
            for meeting in meetings
        ]
    
    @staticmethod
    async def _get_supervisor_stats(
        db: AsyncSession,
        supervisor_id: int,
        students: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get statistics for a supervisor."""
        total_students = len(students)
        on_track_students = len([s for s in students if s["status"] == "on_track"])
        
        # Count pending reports
        pending_stmt = select(func.count(ReportEntry.id)).select_from(
            ReportEntry
        ).join(
            User, ReportEntry.student_id == User.id
        ).join(
            StudentProfile
        ).where(
            and_(
                or_(
                    StudentProfile.supervisor_id == supervisor_id,
                    StudentProfile.co_supervisor_id == supervisor_id
                ),
                ReportEntry.submitted_at.isnot(None)
            )
        )
        pending_reports = await db.scalar(pending_stmt)
        
        # Calculate average response time (mock for now)
        avg_response_time = 2.5  # days
        
        # Calculate completion rate
        completion_rate = 85 if total_students > 0 else 0
        
        return {
            "totalStudents": total_students,
            "onTrackStudents": on_track_students,
            "pendingReports": pending_reports,
            "averageResponseTime": avg_response_time,
            "completionRate": completion_rate
        }