from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.models.phd_plan import VenueType, VenueRating, PaperPlanStatus


class PlannedPaper(Base):
    __tablename__ = "planned_papers"
    
    id = Column(Integer, primary_key=True, index=True)
    phd_plan_id = Column(Integer, ForeignKey("phd_plans.id"), nullable=False)
    paper_number = Column(Integer, nullable=False)  # 1, 2, or 3
    
    # Paper Details
    title = Column(String(500), nullable=False)
    research_question = Column(Text, nullable=False)
    methodology = Column(Text)  # Brief description of planned methodology
    expected_contribution = Column(Text)  # What this paper will contribute
    
    # Publication Planning
    target_venue = Column(String(300))  # Conference/Journal name
    venue_type = Column(Enum(VenueType))
    venue_rating = Column(Enum(VenueRating), nullable=False)  # Must be at least B
    target_completion_date = Column(Date, nullable=False)  # This creates the milestone
    
    # Link to actual research project when created
    research_project_id = Column(Integer, ForeignKey("research_projects.id"))
    
    # Status tracking
    status = Column(Enum(PaperPlanStatus), default=PaperPlanStatus.PLANNED)
    
    # Relationships
    phd_plan = relationship("PhDPlan", back_populates="papers")
    research_project = relationship("ResearchProject", foreign_keys=[research_project_id])