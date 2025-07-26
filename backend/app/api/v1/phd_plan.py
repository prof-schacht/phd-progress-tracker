from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User, UserRole
from app.services.phd_plan_service_async import PhDPlanService
from app.schemas.phd_plan import (
    PhDPlanResponse, PhDPlanUpdate, PhDPlanSubmit,
    PhDPlanApproval, PhDPlanVersionResponse
)
from app.core.exceptions import BadRequestException, NotFoundException, ForbiddenException
import os
from datetime import datetime

router = APIRouter()

@router.get("/users/{user_id}/phd-plan", response_model=PhDPlanResponse)
async def get_phd_plan(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get PhD plan for a user"""
    service = PhDPlanService(db)
    phd_plan = await service.get_phd_plan(user_id, current_user)
    return phd_plan

@router.put("/users/{user_id}/phd-plan", response_model=PhDPlanResponse)
async def update_phd_plan(
    user_id: int,
    plan_data: PhDPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update PhD plan"""
    service = PhDPlanService(db)
    try:
        phd_plan = await service.update_phd_plan(user_id, current_user, plan_data.dict(exclude_unset=True))
        return phd_plan
    except (BadRequestException, ForbiddenException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/users/{user_id}/phd-plan/submit", response_model=PhDPlanResponse)
async def submit_phd_plan(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit PhD plan for approval"""
    service = PhDPlanService(db)
    try:
        phd_plan = await service.submit_for_approval(user_id, current_user)
        return phd_plan
    except (BadRequestException, ForbiddenException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/phd-plans/{plan_id}/approve", response_model=PhDPlanResponse)
async def approve_phd_plan(
    plan_id: int,
    approval_data: PhDPlanApproval,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Approve a PhD plan (supervisors only)"""
    service = PhDPlanService(db)
    try:
        phd_plan = await service.approve_plan(plan_id, current_user, approval_data.comment)
        return phd_plan
    except (BadRequestException, ForbiddenException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/phd-plans/{plan_id}/request-revision", response_model=PhDPlanResponse)
async def request_revision(
    plan_id: int,
    approval_data: PhDPlanApproval,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request revisions for a PhD plan (supervisors only)"""
    service = PhDPlanService(db)
    try:
        phd_plan = await service.request_revision(plan_id, current_user, approval_data.comment)
        return phd_plan
    except (BadRequestException, ForbiddenException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/phd-plans/{plan_id}/history", response_model=List[PhDPlanVersionResponse])
async def get_plan_history(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get version history of a PhD plan"""
    service = PhDPlanService(db)
    try:
        versions = await service.get_plan_history(plan_id, current_user)
        return versions
    except (ForbiddenException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/phd-plans/{plan_id}/proposal-upload")
async def upload_proposal_document(
    plan_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload proposal document (max 5MB)"""
    # Check file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")
    
    # TODO: Implement file upload handling
    # This would save the file and update the phd_plan.proposal_document_id
    
    return {"message": "Proposal uploaded successfully"}

@router.post("/phd-plans/{plan_id}/expose-upload")
async def upload_expose_document(
    plan_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload exposé document (max 5MB)"""
    # Check file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")
    
    # TODO: Implement file upload handling
    # This would save the file and update the phd_plan.expose_document_id
    
    return {"message": "Exposé uploaded successfully"}