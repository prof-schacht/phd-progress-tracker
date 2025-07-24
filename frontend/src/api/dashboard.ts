import apiClient from './client';
import { StudentDashboardData, SupervisorDashboardData } from '../types/dashboard';
import { CurrentPeriodInfo } from '../types/dashboard';

export const dashboardApi = {
  // Student dashboard endpoints
  getStudentDashboard: async (): Promise<StudentDashboardData> => {
    const response = await apiClient.get<StudentDashboardData>('/dashboard/student');
    return response.data;
  },

  getCurrentPeriod: async (): Promise<CurrentPeriodInfo> => {
    const response = await apiClient.get<CurrentPeriodInfo>('/reports/current');
    return response.data;
  },

  // Supervisor dashboard endpoints
  getSupervisorDashboard: async (): Promise<SupervisorDashboardData> => {
    const response = await apiClient.get<SupervisorDashboardData>('/dashboard/supervisor');
    return response.data;
  },

  getPendingReports: async () => {
    const response = await apiClient.get('/reports/supervisor/pending');
    return response.data;
  },
};