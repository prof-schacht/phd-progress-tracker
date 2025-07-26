from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base
import enum


class PhDPlanStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"


class VenueType(str, enum.Enum):
    CONFERENCE = "conference"
    JOURNAL = "journal"


class VenueRating(str, enum.Enum):
    A_STAR = "A*"
    A = "A"
    B = "B"
    C = "C"


class PaperPlanStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    PUBLISHED = "published"


class ApprovalAction(str, enum.Enum):
    APPROVE = "approve"
    REQUEST_REVISION = "request_revision"
    COMMENT = "comment"


class PhDPlan(Base):
    __tablename__ = "phd_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Basic Information
    research_topic = Column(String(500), nullable=False)
    research_question = Column(Text, nullable=False)
    research_field = Column(String(200))
    expected_duration_years = Column(Integer, default=4)
    
    # Proposal & Exposé (both text and files)
    proposal_text = Column(Text)
    proposal_document_id = Column(Integer, ForeignKey("attachments.id"))
    expose_text = Column(Text)
    expose_document_id = Column(Integer, ForeignKey("attachments.id"))
    
    # Status and Workflow
    status = Column(Enum(PhDPlanStatus), default=PhDPlanStatus.DRAFT, nullable=False)
    current_version = Column(Integer, default=1)
    
    # Approval
    submitted_at = Column(DateTime)
    approved_at = Column(DateTime)
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id], back_populates="phd_plan")
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    proposal_document = relationship("Attachment", foreign_keys=[proposal_document_id])
    expose_document = relationship("Attachment", foreign_keys=[expose_document_id])
    papers = relationship("PlannedPaper", back_populates="phd_plan", cascade="all, delete-orphan")
    versions = relationship("PhDPlanVersion", back_populates="phd_plan", cascade="all, delete-orphan")
    approval_comments = relationship("PhDPlanApproval", back_populates="phd_plan", cascade="all, delete-orphan")