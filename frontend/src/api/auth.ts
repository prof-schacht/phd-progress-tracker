import apiClient from './client';
import { LoginRequest, LoginResponse, RegisterRequest, User } from '../types/auth';

export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    console.log('API Base URL:', apiClient.defaults.baseURL);
    console.log('Login endpoint:', '/auth/login/json');
    const response = await apiClient.post<LoginResponse>('/auth/login/json', credentials);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  refreshToken: async (refreshToken: string): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/refresh', null, {
      params: { refresh_token: refreshToken },
    });
    return response.data;
  },
};