export interface ReportPeriod {
  id: number;
  student_id: number;
  period_type: 'BIWEEKLY' | 'QUARTERLY';
  start_date: string;
  end_date: string;
  due_date: string;
  status: ReportStatus;
  reminders_sent: number;
  created_at: string;
  updated_at: string;
}

export enum ReportStatus {
  PENDING = 'PENDING',
  SUBMITTED = 'SUBMITTED',
  REVIEWED = 'REVIEWED',
  OVERDUE = 'OVERDUE',
}

export interface ReportEntry {
  id: number;
  period_id: number;
  student_id: number;
  submitted_at: string;
  accomplishments: string;
  blockers?: string;
  next_period_plan: string;
  time_allocation: TimeAllocation;
  tags?: string[];
  attachments?: number[];
  is_locked: boolean;
  version: number;
}

export interface TimeAllocation {
  research: number;
  writing: number;
  teaching: number;
  meetings: number;
  commercial_projects: number;
  other: number;
}

export interface ReportEntryCreate {
  period_id: number;
  accomplishments: string;
  blockers?: string;
  next_period_plan: string;
  time_allocation: TimeAllocation;
  tags?: string[];
  is_draft: boolean;
}

export interface QuickUpdate {
  status: 'steady_progress' | 'focus_week' | 'blocked';
  note?: string;
}

export interface ReportComment {
  content: string;
  visibility: 'public' | 'private' | 'supervisor_only';
}