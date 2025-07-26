import apiClient from './client';
import { 
  NotificationPreferences, 
  InAppNotification, 
  NotificationList,
  TestNotificationRequest 
} from '../types/notifications';

export const notificationsApi = {
  // Get notification preferences
  getPreferences: async (): Promise<NotificationPreferences> => {
    const response = await apiClient.get<NotificationPreferences>('/notifications/preferences');
    return response.data;
  },

  // Update notification preferences
  updatePreferences: async (preferences: Partial<NotificationPreferences>): Promise<NotificationPreferences> => {
    const response = await apiClient.put<NotificationPreferences>('/notifications/preferences', preferences);
    return response.data;
  },

  // Get notifications list
  getNotifications: async (params?: {
    skip?: number;
    limit?: number;
    unread_only?: boolean;
  }): Promise<NotificationList> => {
    const response = await apiClient.get<NotificationList>('/notifications', { params });
    return response.data;
  },

  // Mark notification as read
  markAsRead: async (notificationId: number): Promise<void> => {
    await apiClient.put(`/notifications/${notificationId}/read`);
  },

  // Send test notification
  sendTest: async (request?: TestNotificationRequest): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>('/notifications/test', request || {});
    return response.data;
  },
};