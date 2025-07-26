from fastapi import APIRouter
from app.api.v1 import auth, users, reports, dashboard, phd_plan, notifications

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(phd_plan.router, prefix="", tags=["phd-plans"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])