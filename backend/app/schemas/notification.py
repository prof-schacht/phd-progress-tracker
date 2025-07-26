"""Notification schemas."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from app.models.notification_preference import EmailFrequency
from app.models.notification_log import NotificationType, NotificationChannel, NotificationStatus


# Notification Preferences
class NotificationPreferenceBase(BaseModel):
    email_enabled: bool = True
    email_frequency: EmailFrequency = EmailFrequency.IMMEDIATE
    slack_enabled: bool = False
    slack_webhook_url: Optional[str] = None
    teams_enabled: bool = False
    teams_webhook_url: Optional[str] = None
    quiet_hours: Dict[str, str] = {}  # {"start": "22:00", "end": "08:00"}
    timezone: str = "Europe/Berlin"


class NotificationPreferenceCreate(NotificationPreferenceBase):
    pass


class NotificationPreferenceUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    email_frequency: Optional[EmailFrequency] = None
    slack_enabled: Optional[bool] = None
    slack_webhook_url: Optional[str] = None
    teams_enabled: Optional[bool] = None
    teams_webhook_url: Optional[str] = None
    quiet_hours: Optional[Dict[str, str]] = None
    timezone: Optional[str] = None


class NotificationPreference(NotificationPreferenceBase):
    user_id: int
    
    class Config:
        from_attributes = True


# Notification Logs
class NotificationLogBase(BaseModel):
    type: NotificationType
    channel: NotificationChannel
    subject: str
    content: str


class NotificationLogCreate(NotificationLogBase):
    user_id: int
    extra_data: Dict[str, Any] = {}


class NotificationLog(NotificationLogBase):
    id: int
    user_id: int
    sent_at: Optional[datetime]
    read_at: Optional[datetime]
    status: NotificationStatus
    extra_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


# In-app notifications
class InAppNotification(BaseModel):
    id: int
    type: NotificationType
    subject: str
    content: str
    created_at: datetime
    read_at: Optional[datetime]
    extra_data: Dict[str, Any]
    
    class Config:
        from_attributes = True


class InAppNotificationList(BaseModel):
    items: List[InAppNotification]
    total: int
    unread_count: int


# Test notification
class TestNotificationRequest(BaseModel):
    email: Optional[str] = None  # If not provided, use current user's email