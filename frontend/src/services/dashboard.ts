import api from './api';

export const dashboardApi = {
  getStudentDashboard: async () => {
    const response = await api.get('/dashboard/student');
    return response.data;
  },

  getSupervisorDashboard: async () => {
    const response = await api.get('/dashboard/supervisor');
    return response.data;
  },

  getCurrentPeriod: async () => {
    const response = await api.get('/reports/current');
    return response.data;
  },
};