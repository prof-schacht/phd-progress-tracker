import api from './api';
import { PhDPlan, PhDPlanUpdate, PhDPlanApproval, PhDPlanVersion } from '../types/phd-plan';

export const phdPlanApi = {
  getPhDPlan: async (userId: number): Promise<PhDPlan> => {
    const response = await api.get(`/users/${userId}/phd-plan`);
    return response.data;
  },

  updatePhDPlan: async (userId: number, data: PhDPlanUpdate): Promise<PhDPlan> => {
    const response = await api.put(`/users/${userId}/phd-plan`, data);
    return response.data;
  },

  submitPhDPlan: async (userId: number): Promise<PhDPlan> => {
    const response = await api.post(`/users/${userId}/phd-plan/submit`);
    return response.data;
  },

  approvePhDPlan: async (planId: number, data: PhDPlanApproval): Promise<PhDPlan> => {
    const response = await api.post(`/phd-plans/${planId}/approve`, data);
    return response.data;
  },

  requestRevision: async (planId: number, data: PhDPlanApproval): Promise<PhDPlan> => {
    const response = await api.post(`/phd-plans/${planId}/request-revision`, data);
    return response.data;
  },

  getPhDPlanHistory: async (planId: number): Promise<PhDPlanVersion[]> => {
    const response = await api.get(`/phd-plans/${planId}/history`);
    return response.data;
  },

  uploadProposal: async (planId: number, file: File): Promise<void> => {
    const formData = new FormData();
    formData.append('file', file);
    await api.post(`/phd-plans/${planId}/proposal-upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  uploadExpose: async (planId: number, file: File): Promise<void> => {
    const formData = new FormData();
    formData.append('file', file);
    await api.post(`/phd-plans/${planId}/expose-upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};