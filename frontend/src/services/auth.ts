import api from './api';
import { LoginCredentials, AuthResponse, User, RegisterRequest } from '../types/auth';

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post('/auth/login/json', credentials);
    const { access_token, refresh_token, token_type } = response.data;
    
    // Store tokens - use same names as AuthContext expects
    localStorage.setItem('access_token', access_token);
    if (refresh_token) {
      localStorage.setItem('refresh_token', refresh_token);
    }
    
    // Backend doesn't return user with login, so we need to fetch it
    // But first we need to set the token in the api instance
    api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    
    // Now fetch the user
    const userResponse = await api.get('/auth/me');
    const user = userResponse.data;
    localStorage.setItem('user', JSON.stringify(user));
    
    return {
      access_token,
      refresh_token,
      token_type,
      expires_in: 3600, // Default to 1 hour
      user
    };
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout');
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};