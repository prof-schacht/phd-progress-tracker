export type EmailFrequency = 'immediate' | 'daily_digest' | 'weekly_digest';
export type NotificationType = 'reminder' | 'alert' | 'feedback' | 'deadline' | 'announcement';
export type NotificationChannel = 'email' | 'slack' | 'teams' | 'in_app';
export type NotificationStatus = 'pending' | 'sent' | 'failed' | 'bounced' | 'read';

export interface NotificationPreferences {
  user_id: number;
  email_enabled: boolean;
  email_frequency: EmailFrequency;
  slack_enabled: boolean;
  slack_webhook_url: string | null;
  teams_enabled: boolean;
  teams_webhook_url: string | null;
  quiet_hours: {
    start?: string;
    end?: string;
  };
  timezone: string;
}

export interface InAppNotification {
  id: number;
  type: NotificationType;
  subject: string;
  content: string;
  created_at: string;
  read_at: string | null;
  extra_data: Record<string, any>;
}

export interface NotificationList {
  items: InAppNotification[];
  total: number;
  unread_count: number;
}

export interface TestNotificationRequest {
  email?: string;
}