from app.models.user import User, UserProfile, UserRole, UserStatus
from app.models.student_profile import StudentProfile, ProgramType, StudentStatus as StudentProfileStatus
from app.models.report_period import ReportPeriod, PeriodType, ReportStatus
from app.models.report_entry import ReportEntry
from app.models.research_project import ResearchProject, ProjectStatus, ProjectType
from app.models.milestone import Milestone, MilestoneType, MilestoneStatus
from app.models.meeting_note import MeetingNote
from app.models.comment import Comment, EntityType, CommentVisibility
from app.models.attachment import Attachment, AttachmentEntityType
from app.models.phd_plan import PhDPlan, PhDPlanStatus, VenueType, VenueRating, PaperPlanStatus, ApprovalAction
from app.models.planned_paper import PlannedPaper
from app.models.phd_plan_version import PhDPlanVersion
from app.models.phd_plan_approval import PhDPlanApproval
from app.models.notification_preference import NotificationPreference, EmailFrequency
from app.models.notification_log import NotificationLog, NotificationType, NotificationChannel, NotificationStatus
from app.models.reminder_schedule import ReminderSchedule, ReminderEntityType

__all__ = [
    # User models
    "User", "UserProfile", "UserRole", "UserStatus",
    # Student profile
    "StudentProfile", "ProgramType", "StudentProfileStatus",
    # Report models
    "ReportPeriod", "PeriodType", "ReportStatus",
    "ReportEntry",
    # Research models
    "ResearchProject", "ProjectStatus", "ProjectType",
    # Milestone models
    "Milestone", "MilestoneType", "MilestoneStatus",
    # Meeting models
    "MeetingNote",
    # Comment models
    "Comment", "EntityType", "CommentVisibility",
    # Attachment models
    "Attachment", "AttachmentEntityType",
    # PhD Plan models
    "PhDPlan", "PhDPlanStatus", "VenueType", "VenueRating", "PaperPlanStatus", "ApprovalAction",
    "PlannedPaper",
    "PhDPlanVersion",
    "PhDPlanApproval",
    # Notification models
    "NotificationPreference", "EmailFrequency",
    "NotificationLog", "NotificationType", "NotificationChannel", "NotificationStatus",
    "ReminderSchedule", "ReminderEntityType"
]