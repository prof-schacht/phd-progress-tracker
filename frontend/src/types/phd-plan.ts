export enum PhDPlanStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  UNDER_REVIEW = 'under_review',
  REVISION_REQUESTED = 'revision_requested',
  APPROVED = 'approved'
}

export enum VenueType {
  CONFERENCE = 'conference',
  JOURNAL = 'journal'
}

export enum VenueRating {
  A_STAR = 'A*',
  A = 'A',
  B = 'B',
  C = 'C'
}

export enum PaperPlanStatus {
  PLANNED = 'planned',
  IN_PROGRESS = 'in_progress',
  SUBMITTED = 'submitted',
  PUBLISHED = 'published'
}

export enum ApprovalAction {
  APPROVE = 'approve',
  REQUEST_REVISION = 'request_revision',
  COMMENT = 'comment'
}

export interface PlannedPaper {
  id?: number;
  paper_number: number;
  title: string;
  research_question: string;
  methodology?: string;
  expected_contribution?: string;
  target_venue?: string;
  venue_type?: VenueType;
  venue_rating: VenueRating;
  target_completion_date: string;
  status?: PaperPlanStatus;
  research_project_id?: number;
}

export interface PhDPlan {
  id: number;
  student_id: number;
  research_topic: string;
  research_question: string;
  research_field?: string;
  expected_duration_years: number;
  proposal_text?: string;
  expose_text?: string;
  status: PhDPlanStatus;
  current_version: number;
  submitted_at?: string;
  approved_at?: string;
  approved_by_id?: number;
  created_at: string;
  updated_at?: string;
  papers: PlannedPaper[];
  proposal_document_id?: number;
  expose_document_id?: number;
}

export interface PhDPlanUpdate {
  research_topic?: string;
  research_question?: string;
  research_field?: string;
  expected_duration_years?: number;
  proposal_text?: string;
  expose_text?: string;
  papers?: PlannedPaper[];
  change_reason?: string;
}

export interface PhDPlanApproval {
  comment: string;
}

export interface PhDPlanVersion {
  id: number;
  phd_plan_id: number;
  version_number: number;
  data_snapshot: any;
  changes_made?: any;
  created_by_id: number;
  created_at: string;
  change_reason?: string;
}

export interface PhDPlanApprovalRecord {
  id: number;
  phd_plan_id: number;
  action: ApprovalAction;
  comment: string;
  reviewer_id: number;
  reviewed_at: string;
}