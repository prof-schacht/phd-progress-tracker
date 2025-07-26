from fastapi import APIRouter
from app.api.v1 import auth, users, reports, phd_plan

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(phd_plan.router, prefix="", tags=["phd-plans"])