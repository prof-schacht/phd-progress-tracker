from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class EmailFrequency(str, Enum):
    IMMEDIATE = "immediate"
    DAILY_DIGEST = "daily_digest"
    WEEKLY_DIGEST = "weekly_digest"


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    
    # Primary key is the user_id (one-to-one with User)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Email preferences
    email_enabled = Column(Boolean, default=True, nullable=False)
    email_frequency = Column(SQLEnum(EmailFrequency), default=EmailFrequency.IMMEDIATE, nullable=False)
    
    # Future channel support
    slack_enabled = Column(Boolean, default=False, nullable=False)
    slack_webhook_url = Column(String(500), nullable=True)
    teams_enabled = Column(Boolean, default=False, nullable=False)
    teams_webhook_url = Column(String(500), nullable=True)
    
    # Timing preferences
    quiet_hours = Column(JSON, default=dict)  # {"start": "22:00", "end": "08:00"}
    timezone = Column(String(50), default="Europe/Berlin", nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notification_preference")
    
    def __repr__(self):
        return f"<NotificationPreference(user_id={self.user_id}, email={self.email_enabled})>"