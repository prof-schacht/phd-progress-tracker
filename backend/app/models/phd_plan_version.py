from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class PhDPlanVersion(Base):
    __tablename__ = "phd_plan_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    phd_plan_id = Column(Integer, ForeignKey("phd_plans.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    
    # Snapshot of all fields at this version
    data_snapshot = Column(JSON, nullable=False)  # Complete state at this version
    changes_made = Column(JSON)  # Diff from previous version
    
    # Who and when
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    change_reason = Column(Text)
    
    # Relationships
    phd_plan = relationship("PhDPlan", back_populates="versions")
    created_by = relationship("User")