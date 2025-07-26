from typing import Optional, Dict, List, Any
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from app.models.report_period import PeriodType, ReportStatus


class TimeAllocation(BaseModel):
    research: int = Field(ge=0, le=100)
    writing: int = Field(ge=0, le=100)
    teaching: int = Field(ge=0, le=100, default=0)
    meetings: int = Field(ge=0, le=100, default=0)
    commercial_projects: int = Field(ge=0, le=100, default=0)
    other: int = Field(ge=0, le=100, default=0)
    
    @validator('other')
    def validate_total(cls, v, values):
        total = (v + values.get('research', 0) + values.get('writing', 0) + 
                values.get('teaching', 0) + values.get('meetings', 0) + 
                values.get('commercial_projects', 0))
        if total != 100:
            raise ValueError(f'Time allocation must sum to 100%, got {total}%')
        return v


class ReportPeriodBase(BaseModel):
    period_type: PeriodType
    start_date: date
    end_date: date
    due_date: date
    

class ReportPeriodCreate(ReportPeriodBase):
    student_id: int
    

class ReportPeriodUpdate(BaseModel):
    status: Optional[ReportStatus] = None
    

class ReportPeriod(ReportPeriodBase):
    id: int
    student_id: int
    status: ReportStatus
    reminders_sent: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReportEntryBase(BaseModel):
    accomplishments: str = Field(min_length=10)  # Reduced for testing
    blockers: Optional[str] = None
    next_period_plan: str = Field(min_length=10)  # Reduced for testing
    time_allocation: TimeAllocation
    tags: Optional[List[str]] = []


class ReportEntryCreate(ReportEntryBase):
    period_id: int
    attachments: Optional[List[int]] = []  # List of attachment IDs
    is_draft: bool = False


class ReportEntryUpdate(BaseModel):
    accomplishments: Optional[str] = Field(None, min_length=10)  # Reduced for testing
    blockers: Optional[str] = None
    next_period_plan: Optional[str] = Field(None, min_length=10)  # Reduced for testing
    time_allocation: Optional[TimeAllocation] = None
    tags: Optional[List[str]] = None
    attachments: Optional[List[int]] = None
    is_draft: Optional[bool] = None


class QuickUpdate(BaseModel):
    status: str = Field(..., pattern="^(steady_progress|focus_week|blocked)$")
    note: Optional[str] = Field(None, max_length=100)


class ReportEntry(ReportEntryBase):
    id: int
    period_id: int
    student_id: int
    submitted_at: datetime
    attachments: List[int]
    is_locked: bool
    version: int
    
    class Config:
        from_attributes = True


class ReportWithPeriod(ReportEntry):
    period: ReportPeriod
    student_name: str
    previous_report: Optional['ReportEntry'] = None


class CurrentPeriodResponse(BaseModel):
    period: ReportPeriod
    current_report: Optional[ReportEntry] = None
    previous_report: Optional[ReportEntry] = None
    auto_populated: Optional[Dict[str, Any]] = None


class ReportComment(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    visibility: str = Field(default="public", pattern="^(public|private|supervisor_only)$")


class CommentResponse(BaseModel):
    id: int
    author_id: int
    author_name: str
    content: str
    visibility: str
    created_at: datetime
    edited_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AcknowledgmentRequest(BaseModel):
    acknowledged: bool = True
    comment: Optional[str] = Field(None, max_length=500)