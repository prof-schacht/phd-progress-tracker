import { User } from './auth';
import { ReportPeriod, ReportEntry } from './report';

// Student Dashboard Types
export interface StudentDashboardData {
  currentPeriod: CurrentPeriodInfo;
  upcomingDeadlines: Deadline[];
  recentFeedback: Comment[];
  researchProjects: ResearchProject[];
  stats: StudentStats;
}

export interface CurrentPeriodInfo {
  period: ReportPeriod;
  currentReport?: ReportEntry;
  previousReport?: ReportEntry;
  autoPopulated?: any;
}

export interface Deadline {
  id: string;
  title: string;
  type: 'report' | 'milestone' | 'meeting';
  dueDate: string;
  status: 'upcoming' | 'overdue' | 'completed';
  daysRemaining?: number;
}

export interface Comment {
  id: number;
  author: User;
  content: string;
  visibility: string;
  createdAt: string;
  editedAt?: string;
}

export interface ResearchProject {
  id: number;
  title: string;
  status: 'planning' | 'in_progress' | 'completed' | 'on_hold';
  progress: number;
  milestones: number;
  completedMilestones: number;
  nextMilestone?: string;
}

export interface StudentStats {
  onTimeSubmissions: number;
  currentStreak: number;
  totalReports: number;
  averageTimeAllocation: TimeAllocation;
}

export interface TimeAllocation {
  research: number;
  writing: number;
  teaching: number;
  meetings: number;
  other: number;
}

// Supervisor Dashboard Types
export interface SupervisorDashboardData {
  students: StudentSummary[];
  alerts: Alert[];
  pendingReviews: PendingReview[];
  upcomingMeetings: Meeting[];
  stats: SupervisorStats;
}

export interface StudentSummary {
  id: number;
  name: string;
  email: string;
  status: 'on_track' | 'at_risk' | 'needs_attention';
  lastReport?: ReportSummary;
  upcomingDeadlines: Deadline[];
  researchPipeline: ResearchProject[];
  program: string;
  yearInProgram: number;
}

export interface ReportSummary {
  id: number;
  periodStart: string;
  periodEnd: string;
  submittedAt: string;
  status: string;
  highlights?: string;
}

export interface Alert {
  id: string;
  type: 'overdue' | 'blocker' | 'milestone' | 'review';
  severity: 'high' | 'medium' | 'low';
  student: User;
  message: string;
  createdAt: string;
  actionRequired: boolean;
}

export interface PendingReview {
  reportId: number;
  studentName: string;
  submittedAt: string;
  daysWaiting: number;
  reportType: 'biweekly' | 'quarterly';
}

export interface Meeting {
  id: number;
  title: string;
  studentName: string;
  scheduledAt: string;
  duration: number;
  location?: string;
  agenda?: string;
}

export interface SupervisorStats {
  totalStudents: number;
  onTrackStudents: number;
  pendingReports: number;
  averageResponseTime: number;
  completionRate: number;
}