"""Dashboard API endpoints."""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.database import get_db
from app.core.deps import get_current_user
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/student", response_model=dict)
async def get_student_dashboard(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get dashboard data for the current student user.
    """
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access this endpoint"
        )
    
    dashboard_data = await DashboardService.get_student_dashboard(
        db, current_user.id
    )
    return dashboard_data


@router.get("/supervisor", response_model=dict)
async def get_supervisor_dashboard(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get dashboard data for the current supervisor user.
    """
    if current_user.role not in ["supervisor", "admin", "system_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can access this endpoint"
        )
    
    dashboard_data = await DashboardService.get_supervisor_dashboard(
        db, current_user.id
    )
    return dashboard_data


@router.get("/admin", response_model=dict)
async def get_admin_dashboard(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get dashboard data for admin users.
    """
    if current_user.role not in ["admin", "system_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint"
        )
    
    # For now, return a simple response
    # This can be expanded later with system-wide statistics
    return {
        "message": "Admin dashboard endpoint",
        "totalUsers": 0,
        "totalStudents": 0,
        "totalSupervisors": 0,
        "systemHealth": "healthy"
    }