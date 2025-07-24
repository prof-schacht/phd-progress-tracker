from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.base import Base


class ReportEntry(Base):
    __tablename__ = "report_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    period_id = Column(Integer, ForeignKey("report_periods.id", ondelete="CASCADE"), nullable=False, unique=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Submission info
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Bi-weekly fields
    accomplishments = Column(Text, nullable=True)
    blockers = Column(Text, nullable=True)
    next_period_plan = Column(Text, nullable=True)
    time_allocation = Column(JSON, default=dict)  # {research: 70, writing: 20, teaching: 10}
    
    # Quarterly additional fields
    quarterly_achievements = Column(JSON, default=dict)
    challenges = Column(Text, nullable=True)
    goals_next_quarter = Column(Text, nullable=True)
    training_completed = Column(Text, nullable=True)
    wellbeing_note = Column(Text, nullable=True)  # Private field
    
    # Common fields
    attachments = Column(JSON, default=list)  # Array of attachment IDs
    tags = Column(JSON, default=list)
    is_locked = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    
    # Relationships
    report_period = relationship("ReportPeriod", foreign_keys=[period_id])
    student = relationship("User", foreign_keys=[student_id])
    # comments = relationship("Comment", back_populates="report_entry")
    
    def __repr__(self):
        return f"<ReportEntry(id={self.id}, period_id={self.period_id}, student_id={self.student_id})>"