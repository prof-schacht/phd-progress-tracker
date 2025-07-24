from datetime import date, datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    DATA_COLLECTION = "data_collection"
    ANALYSIS = "analysis"
    WRITING = "writing"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REVISIONS = "revisions"
    PUBLISHED = "published"
    ABANDONED = "abandoned"


class ProjectType(str, Enum):
    PAPER = "paper"
    THESIS_CHAPTER = "thesis_chapter"
    EXPERIMENT = "experiment"
    CONFERENCE = "conference"
    OTHER = "other"


class ResearchProject(Base):
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Project details
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING)
    project_type = Column(SQLEnum(ProjectType), nullable=False)
    
    # Timeline
    start_date = Column(Date, nullable=False)
    target_completion_date = Column(Date, nullable=False)
    actual_completion_date = Column(Date, nullable=True)
    
    # Additional info
    target_venue = Column(String(255), nullable=True)  # Conference/Journal name
    co_authors = Column(JSON, default=list)  # Array of co-author names
    progress = Column(Integer, default=0)  # 0-100
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata for additional flexible data
    extra_data = Column(JSON, default=dict)  # Renamed from metadata to avoid SQLAlchemy conflict
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    # milestones = relationship("Milestone", back_populates="research_project")
    # comments = relationship("Comment", back_populates="research_project")
    
    # Index for performance
    __table_args__ = (
        # Index will be created in migration: CREATE INDEX idx_research_projects_status ON research_projects(student_id, status);
    )
    
    def __repr__(self):
        return f"<ResearchProject(id={self.id}, title='{self.title}', status={self.status.value})>"