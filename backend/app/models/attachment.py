from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class AttachmentEntityType(str, Enum):
    REPORT = "report"
    PROJECT = "project"
    MEETING = "meeting"
    COMMENT = "comment"


class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # File information
    filename = Column(String(255), nullable=False)  # Stored filename (UUID-based)
    original_name = Column(String(255), nullable=False)  # Original filename
    mime_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)  # File size in bytes
    path = Column(String(500), nullable=False)  # Storage path
    
    # Ownership
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Polymorphic association
    entity_type = Column(SQLEnum(AttachmentEntityType), nullable=False)
    entity_id = Column(Integer, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    uploader = relationship("User", foreign_keys=[uploaded_by])
    
    def __repr__(self):
        return f"<Attachment(id={self.id}, original_name='{self.original_name}', entity_type={self.entity_type.value})>"