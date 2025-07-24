from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_student, require_supervisor
from app.models import User, UserRole, ReportStatus, ReportPeriod, ReportEntry
from app.schemas.report import (
    ReportPeriod as ReportPeriodSchema,
    ReportEntry as ReportEntrySchema,
    ReportEntryCreate, ReportEntryUpdate,
    CurrentPeriodResponse, ReportWithPeriod, QuickUpdate,
    ReportComment, CommentResponse, AcknowledgmentRequest
)
from app.services.report import ReportService

router = APIRouter()


@router.get("/current", response_model=CurrentPeriodResponse)
async def get_current_period(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_student)
) -> Any:
    """
    Get current report period for logged-in student.
    Auto-creates period if none exists.
    Includes previous period data for auto-population.
    """
    # Get or create current period
    current_period = await ReportService.get_or_create_current_period(
        db, current_user.id
    )
    
    # Get current report if exists
    current_report = None
    reports = await db.execute(
        select(ReportEntry).where(
            ReportEntry.period_id == current_period.id,
            ReportEntry.student_id == current_user.id
        )
    )
    current_report = reports.scalar_one_or_none()
    
    # Get previous report for auto-population
    previous_report = await ReportService.get_previous_report(
        db, current_user.id, current_period.start_date
    )
    
    # Get auto-population data
    auto_populated = None
    if not current_report and previous_report:
        auto_populated = await ReportService.auto_populate_from_previous(
            db, current_user.id, current_period
        )
    
    return CurrentPeriodResponse(
        period=current_period,
        current_report=current_report,
        previous_report=previous_report,
        auto_populated=auto_populated
    )


@router.get("/periods", response_model=List[ReportPeriodSchema])
async def get_report_periods(
    status: Optional[ReportStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    List all report periods for a student.
    Students see their own, supervisors see their students'.
    """
    if current_user.role == UserRole.STUDENT:
        periods = await ReportService.get_report_periods(
            db, current_user.id, status, limit, skip
        )
    else:
        # For supervisors, this would need to be modified to show all their students
        # For now, return empty list
        periods = []
    
    return periods


@router.post("/submit", response_model=ReportEntrySchema)
async def submit_report(
    report_data: ReportEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_student)
) -> Any:
    """
    Submit or update report for current period.
    Supports draft saves (partial data).
    Auto-populates from previous period.
    """
    # Verify the period belongs to the student
    period = await db.get(ReportPeriod, report_data.period_id)
    if not period or period.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit report for this period"
        )
    
    # Check if period is still open
    if period.status not in [ReportStatus.PENDING, ReportStatus.SUBMITTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report period is closed"
        )
    
    report = await ReportService.submit_report(
        db, current_user.id, report_data
    )
    
    return report


@router.put("/{report_id}/quick-update", response_model=ReportEntrySchema)
async def quick_update_report(
    update_data: QuickUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_student)
) -> Any:
    """
    Quick status update with optional short note.
    Creates a minimal report for the current period.
    """
    report = await ReportService.quick_update_report(
        db, None, current_user.id, update_data
    )
    return report


@router.get("/{report_id}", response_model=ReportWithPeriod)
async def get_report_detail(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get specific report details.
    Students can view their own, supervisors can view their students'.
    """
    report = await ReportService.get_report_by_id(db, report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check access permissions
    if current_user.role == UserRole.STUDENT:
        if report.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access this report"
            )
    elif current_user.role == UserRole.SUPERVISOR:
        # Check if supervisor has access to this student
        from app.models import StudentProfile
        from sqlalchemy import select, or_
        
        result = await db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == report.student_id,
                or_(
                    StudentProfile.supervisor_id == current_user.id,
                    StudentProfile.co_supervisor_id == current_user.id
                )
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access this student's report"
            )
    
    # Get student name
    student = await db.get(User, report.student_id)
    
    # Get previous report for context
    previous = await ReportService.get_previous_report(
        db, report.student_id, report.report_period.start_date
    )
    
    return ReportWithPeriod(
        **report.__dict__,
        period=report.report_period,
        student_name=student.full_name,
        previous_report=previous
    )


@router.post("/{report_id}/comment", response_model=CommentResponse)
async def add_comment_to_report(
    report_id: int,
    comment_data: ReportComment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Add comment to a report.
    Students can comment on their own reports.
    Supervisors can comment on their students' reports.
    """
    # Verify access to report
    report = await ReportService.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check permissions (similar to get_report_detail)
    has_access = False
    if current_user.role == UserRole.STUDENT and report.student_id == current_user.id:
        has_access = True
    elif current_user.role in [UserRole.SUPERVISOR, UserRole.ADMIN]:
        # Check supervisor relationship
        from app.models import StudentProfile
        from sqlalchemy import select, or_
        
        result = await db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == report.student_id,
                or_(
                    StudentProfile.supervisor_id == current_user.id,
                    StudentProfile.co_supervisor_id == current_user.id
                )
            )
        )
        if result.scalar_one_or_none():
            has_access = True
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot comment on this report"
        )
    
    comment = await ReportService.add_comment_to_report(
        db, report_id, current_user.id,
        comment_data.content, comment_data.visibility
    )
    
    return CommentResponse(
        id=comment.id,
        author_id=comment.author_id,
        author_name=current_user.full_name,
        content=comment.content,
        visibility=comment.visibility,
        created_at=comment.created_at,
        edited_at=comment.edited_at
    )


@router.put("/{report_id}/acknowledge")
async def acknowledge_report(
    report_id: int,
    ack_data: AcknowledgmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_supervisor)
) -> Any:
    """
    Supervisor acknowledges a report.
    Adds an acknowledgment comment.
    """
    success = await ReportService.acknowledge_report(
        db, report_id, current_user.id, ack_data.comment
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot acknowledge this report"
        )
    
    return {"message": "Report acknowledged successfully"}


@router.get("/supervisor/pending", response_model=List[Dict[str, Any]])
async def get_pending_reports_for_supervisor(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_supervisor)
) -> Any:
    """
    Get all pending reports for students supervised by current user.
    """
    reports = await ReportService.get_student_reports_for_supervisor(
        db, current_user.id, ReportStatus.SUBMITTED
    )
    
    # Convert to serializable format
    result = []
    for report_data in reports:
        result.append({
            "report_id": report_data["report"].id,
            "period_id": report_data["period"].id,
            "student_id": report_data["student"].id,
            "student_name": report_data["student"].full_name,
            "period_start": report_data["period"].start_date.isoformat(),
            "period_end": report_data["period"].end_date.isoformat(),
            "due_date": report_data["period"].due_date.isoformat(),
            "submitted_at": report_data["report"].submitted_at.isoformat(),
            "accomplishments": report_data["report"].accomplishments[:100] + "..." if len(report_data["report"].accomplishments) > 100 else report_data["report"].accomplishments
        })
    
    return result