import api from './api';
import { Report, ReportFormData, ReportPeriod } from '../types/report';

export const reportsApi = {
  getCurrentPeriod: async (): Promise<ReportPeriod> => {
    const response = await api.get('/reports/current');
    return response.data;
  },

  getReports: async (params?: { period_type?: string; status?: string }): Promise<Report[]> => {
    const response = await api.get('/reports/periods', { params });
    return response.data;
  },

  getReport: async (id: number): Promise<Report> => {
    const response = await api.get(`/reports/${id}`);
    return response.data;
  },

  submitReport: async (data: ReportFormData): Promise<Report> => {
    const response = await api.post('/reports/submit', data);
    return response.data;
  },

  updateReport: async (id: number, data: Partial<ReportFormData>): Promise<Report> => {
    const response = await api.patch(`/reports/${id}`, data);
    return response.data;
  },
};