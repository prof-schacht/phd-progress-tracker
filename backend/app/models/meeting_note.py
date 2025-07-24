from datetime import date, datetime
from sqlalchemy import Column, Integer, Text, Date, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.base import Base


class MeetingNote(Base):
    __tablename__ = "meeting_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Optional link to report period
    period_id = Column(Integer, ForeignKey("report_periods.id", ondelete="SET NULL"), nullable=True)
    
    # Meeting details
    meeting_date = Column(DateTime, nullable=False)
    agenda = Column(Text, nullable=True)
    
    # Structured data
    decisions = Column(JSON, default=list)  # Array of decision objects
    action_items = Column(JSON, default=list)  # Array of {task, owner, dueDate, status}
    
    # Follow-up
    next_meeting_date = Column(Date, nullable=True)
    
    # Privacy
    is_private = Column(Boolean, default=False)
    
    # Attachments
    attachments = Column(JSON, default=list)  # Array of attachment IDs
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    supervisor = relationship("User", foreign_keys=[supervisor_id])
    report_period = relationship("ReportPeriod", foreign_keys=[period_id])
    # comments = relationship("Comment", back_populates="meeting_note")
    
    def __repr__(self):
        return f"<MeetingNote(id={self.id}, student_id={self.student_id}, meeting_date={self.meeting_date})>"