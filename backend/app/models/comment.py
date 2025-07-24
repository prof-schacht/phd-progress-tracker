from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.base import Base


class EntityType(str, Enum):
    REPORT = "report"
    PROJECT = "project"
    MILESTONE = "milestone"
    MEETING = "meeting"


class CommentVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    SUPERVISOR_ONLY = "supervisor_only"


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Polymorphic association
    entity_type = Column(SQLEnum(EntityType), nullable=False)
    entity_id = Column(Integer, nullable=False)
    
    # Comment details
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    visibility = Column(SQLEnum(CommentVisibility), nullable=False, default=CommentVisibility.PUBLIC)
    
    # Threading support
    parent_comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    edited_at = Column(DateTime, nullable=True)
    
    # Relationships
    author = relationship("User", foreign_keys=[author_id])
    parent_comment = relationship("Comment", remote_side=[id], backref="replies")
    
    # Index for performance
    __table_args__ = (
        # Index will be created in migration: CREATE INDEX idx_comments_entity ON comments(entity_type, entity_id);
    )
    
    def __repr__(self):
        return f"<Comment(id={self.id}, entity_type={self.entity_type.value}, entity_id={self.entity_id})>"