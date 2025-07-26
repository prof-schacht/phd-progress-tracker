from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base
from app.models.phd_plan import ApprovalAction


class PhDPlanApproval(Base):
    __tablename__ = "phd_plan_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    phd_plan_id = Column(Integer, ForeignKey("phd_plans.id"), nullable=False)
    
    # Approval details
    action = Column(Enum(ApprovalAction), nullable=False)
    comment = Column(Text, nullable=False)
    
    # Who and when
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    phd_plan = relationship("PhDPlan", back_populates="approval_comments")
    reviewer = relationship("User")