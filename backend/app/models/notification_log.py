from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class NotificationType(str, Enum):
    REMINDER = "reminder"
    ALERT = "alert"
    FEEDBACK = "feedback"
    DEADLINE = "deadline"
    ANNOUNCEMENT = "announcement"


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    IN_APP = "in_app"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BOUNCED = "bounced"
    READ = "read"


class NotificationLog(Base):
    __tablename__ = "notification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Notification details
    type = Column(SQLEnum(NotificationType), nullable=False)
    channel = Column(SQLEnum(NotificationChannel), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Status tracking
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    
    # Additional data
    extra_data = Column(JSON, default=dict)  # For storing channel-specific info
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="notification_logs")
    
    def __repr__(self):
        return f"<NotificationLog(id={self.id}, user_id={self.user_id}, type={self.type})>"