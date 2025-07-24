from datetime import date
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON, ARRAY, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class ProgramType(str, Enum):
    PHD = "phd"
    MPHIL = "mphil"
    MASTERS = "masters"


class StudentStatus(str, Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    GRADUATED = "graduated"
    WITHDRAWN = "withdrawn"


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    # Primary key is the user_id (one-to-one with User)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Program information
    program_name = Column(String(255), nullable=False)
    program_type = Column(SQLEnum(ProgramType), nullable=False, default=ProgramType.PHD)
    start_date = Column(Date, nullable=False)
    expected_end_date = Column(Date, nullable=False)
    actual_end_date = Column(Date, nullable=True)
    
    # Supervision
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    co_supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status and research
    status = Column(SQLEnum(StudentStatus), nullable=False, default=StudentStatus.ACTIVE)
    research_area = Column(String(500), nullable=False)
    thesis_title = Column(String(500), nullable=True)
    
    # Additional data
    tags = Column(JSON, default=list)  # Store as JSON array
    extra_data = Column(JSON, default=dict)  # Renamed from metadata to avoid SQLAlchemy conflict
    
    # Relationships
    student = relationship("User", foreign_keys=[user_id], back_populates="student_profile")
    supervisor = relationship("User", foreign_keys=[supervisor_id])
    co_supervisor = relationship("User", foreign_keys=[co_supervisor_id])
    
    # One-to-many relationships (to be defined when other models are created)
    # report_periods = relationship("ReportPeriod", back_populates="student_profile")
    # research_projects = relationship("ResearchProject", back_populates="student_profile")
    # milestones = relationship("Milestone", back_populates="student_profile")
    # meeting_notes = relationship("MeetingNote", back_populates="student_profile")
    
    def __repr__(self):
        return f"<StudentProfile(user_id={self.user_id}, program={self.program_type.value}, status={self.status.value})>"