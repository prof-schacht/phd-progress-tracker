import apiClient from './client';
import { ReportPeriod, ReportEntry, ReportEntryCreate, QuickUpdate, ReportComment } from '../types/report';

export const reportsApi = {
  // Get report periods
  getPeriods: async (status?: string) => {
    const params = status ? { status } : {};
    const response = await apiClient.get<ReportPeriod[]>('/reports/periods', { params });
    return response.data;
  },

  // Submit report
  submitReport: async (data: ReportEntryCreate) => {
    const response = await apiClient.post<ReportEntry>('/reports/submit', data);
    return response.data;
  },

  // Quick update
  quickUpdate: async (periodId: number, data: QuickUpdate) => {
    const response = await apiClient.put(`/reports/${periodId}/quick-update`, data);
    return response.data;
  },

  // Get report details
  getReport: async (reportId: number) => {
    const response = await apiClient.get(`/reports/${reportId}`);
    return response.data;
  },

  // Add comment
  addComment: async (reportId: number, data: ReportComment) => {
    const response = await apiClient.post(`/reports/${reportId}/comment`, data);
    return response.data;
  },

  // Acknowledge report (supervisor)
  acknowledgeReport: async (reportId: number, comment?: string) => {
    const response = await apiClient.put(`/reports/${reportId}/acknowledge`, {
      acknowledged: true,
      comment,
    });
    return response.data;
  },
};