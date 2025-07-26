from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from app.core.base import Base


class ReminderEntityType(str, Enum):
    REPORT_PERIOD = "report_period"
    MILESTONE = "milestone"
    MEETING = "meeting"
    QUARTERLY_REVIEW = "quarterly_review"


class ReminderSchedule(Base):
    __tablename__ = "reminder_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # What to remind about
    entity_type = Column(SQLEnum(ReminderEntityType), nullable=False)
    entity_id = Column(Integer, nullable=False, index=True)
    
    # When to send
    scheduled_for = Column(DateTime, nullable=False, index=True)
    reminder_type = Column(String(50), nullable=False)  # 'T-3days', 'T-0', 'T+2days'
    
    # Processing status
    processed = Column(Boolean, default=False, nullable=False, index=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Who to notify
    user_id = Column(Integer, nullable=False, index=True)
    include_supervisor = Column(Boolean, default=False, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ReminderSchedule(id={self.id}, entity={self.entity_type}, scheduled={self.scheduled_for})>"