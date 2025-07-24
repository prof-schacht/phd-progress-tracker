from datetime import date, datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class MilestoneType(str, Enum):
    THESIS_PROPOSAL = "thesis_proposal"
    COMPREHENSIVE_EXAM = "comprehensive_exam"
    CONFERENCE_SUBMISSION = "conference_submission"
    PAPER_SUBMISSION = "paper_submission"
    DEFENSE = "defense"
    CUSTOM = "custom"


class MilestoneStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    POSTPONED = "postponed"


class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Milestone details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(SQLEnum(MilestoneType), nullable=False, default=MilestoneType.CUSTOM)
    
    # Dates
    due_date = Column(Date, nullable=False, index=True)
    completed_date = Column(Date, nullable=True)
    
    # Status
    status = Column(SQLEnum(MilestoneStatus), nullable=False, default=MilestoneStatus.PLANNED)
    is_public = Column(Boolean, default=True)
    
    # Optional link to research project
    related_project_id = Column(Integer, ForeignKey("research_projects.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    research_project = relationship("ResearchProject", foreign_keys=[related_project_id])
    # comments = relationship("Comment", back_populates="milestone")
    
    # Index for performance
    __table_args__ = (
        # Index will be created in migration: CREATE INDEX idx_milestones_due_date ON milestones(due_date, status);
    )
    
    def __repr__(self):
        return f"<Milestone(id={self.id}, title='{self.title}', type={self.type.value}, status={self.status.value})>"