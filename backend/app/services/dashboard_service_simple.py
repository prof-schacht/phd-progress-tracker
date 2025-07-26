"""Simplified dashboard service for testing."""

from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dashboard_service import DashboardService


class SimpleDashboardService:
    """Simplified dashboard service."""
    
    @staticmethod
    async def get_supervisor_dashboard(
        db: AsyncSession,
        supervisor_id: int
    ) -> Dict[str, Any]:
        """Get simplified supervisor dashboard data."""
        return {
            "students": [],
            "alerts": [],
            "pendingReviews": [],
            "upcomingMeetings": [],
            "stats": {
                "totalStudents": 0,
                "onTrackStudents": 0,
                "pendingReports": 0,
                "averageResponseTime": 0,
                "completionRate": 0
            }
        }