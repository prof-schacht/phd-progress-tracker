from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class PeriodType(str, Enum):
    BIWEEKLY = "biweekly"
    QUARTERLY = "quarterly"


class ReportStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    OVERDUE = "overdue"
    EXCUSED = "excused"


class ReportPeriod(Base):
    __tablename__ = "report_periods"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Period information
    period_type = Column(SQLEnum(PeriodType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Status tracking
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.PENDING)
    reminders_sent = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    # report_entry = relationship("ReportEntry", back_populates="report_period", uselist=False)
    # meeting_notes = relationship("MeetingNote", back_populates="report_period")
    
    # Indexes will be created in migration
    __table_args__ = (
        # Index for finding periods by student and status
        # Will be created as: CREATE INDEX idx_report_periods_student_status ON report_periods(student_id, status);
    )
    
    def __repr__(self):
        return f"<ReportPeriod(id={self.id}, student_id={self.student_id}, type={self.period_type.value}, status={self.status.value})>"