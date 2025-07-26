from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import (
    PhDPlan, PhDPlanStatus, PlannedPaper, PhDPlanVersion, 
    PhDPlanApproval, ApprovalAction, User, UserRole, Milestone, MilestoneType, MilestoneStatus
)
from app.core.exceptions import BadRequestException, NotFoundException, ForbiddenException
import json


class PhDPlanService:
    def __init__(self, db: Session):
        self.db = db

    def get_phd_plan(self, user_id: int, current_user: User) -> Optional[PhDPlan]:
        """Get PhD plan for a specific user"""
        # Check permissions
        if current_user.id != user_id and current_user.role not in [UserRole.SUPERVISOR, UserRole.ADMIN]:
            raise ForbiddenException("You don't have permission to view this PhD plan")
        
        phd_plan = self.db.query(PhDPlan).filter(PhDPlan.student_id == user_id).first()
        if not phd_plan and current_user.id == user_id:
            # Auto-create draft plan for the student
            phd_plan = self.create_draft_plan(user_id)
        
        return phd_plan

    def create_draft_plan(self, student_id: int) -> PhDPlan:
        """Create a new draft PhD plan"""
        phd_plan = PhDPlan(
            student_id=student_id,
            research_topic="",
            research_question="",
            status=PhDPlanStatus.DRAFT
        )
        self.db.add(phd_plan)
        self.db.commit()
        self.db.refresh(phd_plan)
        return phd_plan

    def update_phd_plan(
        self, 
        user_id: int, 
        current_user: User,
        data: Dict[str, Any]
    ) -> PhDPlan:
        """Update PhD plan"""
        # Only students can update their own plans
        if current_user.id != user_id:
            raise ForbiddenException("You can only update your own PhD plan")
        
        phd_plan = self.get_phd_plan(user_id, current_user)
        if not phd_plan:
            phd_plan = self.create_draft_plan(user_id)
        
        # Check if plan is editable
        if phd_plan.status not in [PhDPlanStatus.DRAFT, PhDPlanStatus.REVISION_REQUESTED]:
            raise BadRequestException("PhD plan can only be edited in DRAFT or REVISION_REQUESTED status")
        
        # Create version snapshot before updating
        self._create_version_snapshot(phd_plan, current_user, data.get('change_reason', 'Updated PhD plan'))
        
        # Update basic fields
        if 'research_topic' in data:
            phd_plan.research_topic = data['research_topic']
        if 'research_question' in data:
            phd_plan.research_question = data['research_question']
        if 'research_field' in data:
            phd_plan.research_field = data['research_field']
        if 'expected_duration_years' in data:
            phd_plan.expected_duration_years = data['expected_duration_years']
        if 'proposal_text' in data:
            phd_plan.proposal_text = data['proposal_text']
        if 'expose_text' in data:
            phd_plan.expose_text = data['expose_text']
        
        # Update papers
        if 'papers' in data:
            self._update_papers(phd_plan, data['papers'])
        
        phd_plan.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(phd_plan)
        
        return phd_plan

    def submit_for_approval(self, user_id: int, current_user: User) -> PhDPlan:
        """Submit PhD plan for approval"""
        if current_user.id != user_id:
            raise ForbiddenException("You can only submit your own PhD plan")
        
        phd_plan = self.get_phd_plan(user_id, current_user)
        if not phd_plan:
            raise NotFoundException("PhD plan not found")
        
        # Validate before submission
        errors = self._validate_plan_for_submission(phd_plan)
        if errors:
            raise BadRequestException(f"PhD plan validation failed: {', '.join(errors)}")
        
        phd_plan.status = PhDPlanStatus.SUBMITTED
        phd_plan.submitted_at = datetime.utcnow()
        
        # Create milestones for papers
        self._create_paper_milestones(phd_plan)
        
        self.db.commit()
        self.db.refresh(phd_plan)
        
        return phd_plan

    def approve_plan(
        self, 
        plan_id: int, 
        current_user: User, 
        comment: str
    ) -> PhDPlan:
        """Approve a PhD plan"""
        if current_user.role not in [UserRole.SUPERVISOR, UserRole.ADMIN]:
            raise ForbiddenException("Only supervisors can approve PhD plans")
        
        phd_plan = self.db.query(PhDPlan).filter(PhDPlan.id == plan_id).first()
        if not phd_plan:
            raise NotFoundException("PhD plan not found")
        
        if phd_plan.status != PhDPlanStatus.SUBMITTED:
            raise BadRequestException("Only submitted plans can be approved")
        
        # Create approval record
        approval = PhDPlanApproval(
            phd_plan_id=plan_id,
            action=ApprovalAction.APPROVE,
            comment=comment,
            reviewer_id=current_user.id
        )
        self.db.add(approval)
        
        # Update plan status
        phd_plan.status = PhDPlanStatus.APPROVED
        phd_plan.approved_at = datetime.utcnow()
        phd_plan.approved_by_id = current_user.id
        
        self.db.commit()
        self.db.refresh(phd_plan)
        
        return phd_plan

    def request_revision(
        self, 
        plan_id: int, 
        current_user: User, 
        comment: str
    ) -> PhDPlan:
        """Request revisions for a PhD plan"""
        if current_user.role not in [UserRole.SUPERVISOR, UserRole.ADMIN]:
            raise ForbiddenException("Only supervisors can request revisions")
        
        phd_plan = self.db.query(PhDPlan).filter(PhDPlan.id == plan_id).first()
        if not phd_plan:
            raise NotFoundException("PhD plan not found")
        
        if phd_plan.status != PhDPlanStatus.SUBMITTED:
            raise BadRequestException("Only submitted plans can have revisions requested")
        
        # Create revision request record
        approval = PhDPlanApproval(
            phd_plan_id=plan_id,
            action=ApprovalAction.REQUEST_REVISION,
            comment=comment,
            reviewer_id=current_user.id
        )
        self.db.add(approval)
        
        # Update plan status
        phd_plan.status = PhDPlanStatus.REVISION_REQUESTED
        
        self.db.commit()
        self.db.refresh(phd_plan)
        
        return phd_plan

    def get_plan_history(self, plan_id: int, current_user: User) -> List[PhDPlanVersion]:
        """Get version history of a PhD plan"""
        phd_plan = self.db.query(PhDPlan).filter(PhDPlan.id == plan_id).first()
        if not phd_plan:
            raise NotFoundException("PhD plan not found")
        
        # Check permissions
        if current_user.id != phd_plan.student_id and current_user.role not in [UserRole.SUPERVISOR, UserRole.ADMIN]:
            raise ForbiddenException("You don't have permission to view this plan's history")
        
        versions = self.db.query(PhDPlanVersion).filter(
            PhDPlanVersion.phd_plan_id == plan_id
        ).order_by(PhDPlanVersion.version_number.desc()).all()
        
        return versions

    def _validate_plan_for_submission(self, phd_plan: PhDPlan) -> List[str]:
        """Validate PhD plan before submission"""
        errors = []
        
        if not phd_plan.research_topic:
            errors.append("Research topic is required")
        if not phd_plan.research_question:
            errors.append("Research question is required")
        if not phd_plan.papers or len(phd_plan.papers) != 3:
            errors.append("Exactly 3 planned papers are required")
        
        for paper in phd_plan.papers:
            if not paper.title:
                errors.append(f"Paper {paper.paper_number}: Title is required")
            if not paper.research_question:
                errors.append(f"Paper {paper.paper_number}: Research question is required")
            if not paper.target_completion_date:
                errors.append(f"Paper {paper.paper_number}: Target completion date is required")
            if not paper.venue_rating:
                errors.append(f"Paper {paper.paper_number}: Venue rating is required")
        
        return errors

    def _create_version_snapshot(self, phd_plan: PhDPlan, user: User, change_reason: str):
        """Create a version snapshot of the PhD plan"""
        # Create snapshot of current state
        snapshot = {
            'research_topic': phd_plan.research_topic,
            'research_question': phd_plan.research_question,
            'research_field': phd_plan.research_field,
            'expected_duration_years': phd_plan.expected_duration_years,
            'proposal_text': phd_plan.proposal_text,
            'expose_text': phd_plan.expose_text,
            'papers': [
                {
                    'paper_number': p.paper_number,
                    'title': p.title,
                    'research_question': p.research_question,
                    'methodology': p.methodology,
                    'expected_contribution': p.expected_contribution,
                    'target_venue': p.target_venue,
                    'venue_type': p.venue_type.value if p.venue_type else None,
                    'venue_rating': p.venue_rating.value if p.venue_rating else None,
                    'target_completion_date': p.target_completion_date.isoformat() if p.target_completion_date else None
                }
                for p in phd_plan.papers
            ]
        }
        
        # Get previous version for diff
        last_version = self.db.query(PhDPlanVersion).filter(
            PhDPlanVersion.phd_plan_id == phd_plan.id
        ).order_by(PhDPlanVersion.version_number.desc()).first()
        
        changes_made = {}
        if last_version:
            last_data = last_version.data_snapshot
            # Simple diff - just track which fields changed
            for key, value in snapshot.items():
                if key != 'papers' and last_data.get(key) != value:
                    changes_made[key] = {'old': last_data.get(key), 'new': value}
        
        version = PhDPlanVersion(
            phd_plan_id=phd_plan.id,
            version_number=phd_plan.current_version,
            data_snapshot=snapshot,
            changes_made=changes_made,
            created_by_id=user.id,
            change_reason=change_reason
        )
        self.db.add(version)
        
        # Increment version number
        phd_plan.current_version += 1

    def _update_papers(self, phd_plan: PhDPlan, papers_data: List[Dict[str, Any]]):
        """Update planned papers"""
        # Remove existing papers
        for paper in phd_plan.papers:
            self.db.delete(paper)
        
        # Add new papers
        for paper_data in papers_data:
            paper = PlannedPaper(
                phd_plan_id=phd_plan.id,
                paper_number=paper_data['paper_number'],
                title=paper_data['title'],
                research_question=paper_data['research_question'],
                methodology=paper_data.get('methodology'),
                expected_contribution=paper_data.get('expected_contribution'),
                target_venue=paper_data.get('target_venue'),
                venue_type=paper_data.get('venue_type'),
                venue_rating=paper_data.get('venue_rating'),
                target_completion_date=datetime.fromisoformat(paper_data['target_completion_date']) if paper_data.get('target_completion_date') else None
            )
            self.db.add(paper)

    def _create_paper_milestones(self, phd_plan: PhDPlan):
        """Create milestones for each planned paper"""
        for paper in phd_plan.papers:
            # Check if milestone already exists
            existing = self.db.query(Milestone).filter(
                Milestone.student_id == phd_plan.student_id,
                Milestone.title == f"Paper {paper.paper_number}: {paper.title}"
            ).first()
            
            if not existing:
                milestone = Milestone(
                    student_id=phd_plan.student_id,
                    title=f"Paper {paper.paper_number}: {paper.title}",
                    description=f"Complete and submit paper: {paper.research_question}",
                    due_date=paper.target_completion_date,
                    milestone_type=MilestoneType.PAPER_SUBMISSION,
                    status=MilestoneStatus.PLANNED
                )
                self.db.add(milestone)