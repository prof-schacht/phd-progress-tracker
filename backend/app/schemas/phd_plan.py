from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models.phd_plan import PhDPlanStatus, VenueType, VenueRating, PaperPlanStatus, ApprovalAction


class PlannedPaperBase(BaseModel):
    paper_number: int = Field(..., ge=1, le=3)
    title: str = Field(..., min_length=5, max_length=500)
    research_question: str = Field(..., min_length=10)
    methodology: Optional[str] = None
    expected_contribution: Optional[str] = None
    target_venue: Optional[str] = Field(None, max_length=300)
    venue_type: Optional[VenueType] = None
    venue_rating: VenueRating
    target_completion_date: date

    @validator('venue_rating')
    def validate_venue_rating(cls, v):
        if v == VenueRating.C:
            raise ValueError("Papers must target venues rated B or higher")
        return v


class PlannedPaperResponse(PlannedPaperBase):
    id: int
    status: PaperPlanStatus
    research_project_id: Optional[int] = None

    class Config:
        from_attributes = True


class PhDPlanBase(BaseModel):
    research_topic: str = Field(..., min_length=5, max_length=500)
    research_question: str = Field(..., min_length=20)
    research_field: Optional[str] = Field(None, max_length=200)
    expected_duration_years: int = Field(4, ge=3, le=7)
    proposal_text: Optional[str] = None
    expose_text: Optional[str] = None


class PhDPlanUpdate(PhDPlanBase):
    papers: Optional[List[PlannedPaperBase]] = None
    change_reason: Optional[str] = None

    @validator('papers')
    def validate_papers(cls, v):
        if v and len(v) != 3:
            raise ValueError("Exactly 3 papers must be planned")
        return v


class PhDPlanSubmit(BaseModel):
    pass  # No additional fields needed for submission


class PhDPlanApproval(BaseModel):
    comment: str = Field(..., min_length=10)


class PhDPlanResponse(BaseModel):
    id: int
    student_id: int
    research_topic: str  # Allow empty for drafts
    research_question: str  # Allow empty for drafts
    research_field: Optional[str] = None
    expected_duration_years: int
    proposal_text: Optional[str] = None
    expose_text: Optional[str] = None
    status: PhDPlanStatus
    current_version: int
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    approved_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    papers: List[PlannedPaperResponse] = []
    proposal_document_id: Optional[int] = None
    expose_document_id: Optional[int] = None

    class Config:
        from_attributes = True


class PhDPlanVersionResponse(BaseModel):
    id: int
    phd_plan_id: int
    version_number: int
    data_snapshot: Dict[str, Any]
    changes_made: Optional[Dict[str, Any]] = None
    created_by_id: int
    created_at: datetime
    change_reason: Optional[str] = None

    class Config:
        from_attributes = True


class PhDPlanApprovalResponse(BaseModel):
    id: int
    phd_plan_id: int
    action: ApprovalAction
    comment: str
    reviewer_id: int
    reviewed_at: datetime

    class Config:
        from_attributes = True