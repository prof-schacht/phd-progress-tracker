export enum UserRole {
  STUDENT = 'student',
  SUPERVISOR = 'supervisor',
  ADMIN = 'admin',
  SYSTEM_ADMIN = 'system_admin',
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  status: string;
  created_at: string;
  updated_at: string;
  last_login?: string;
  profile?: UserProfile;
  student_profile?: StudentProfile;
}

export interface UserProfile {
  id: number;
  user_id: number;
  department?: string;
  phone?: string;
  office_location?: string;
  bio?: string;
  avatar_url?: string;
  notification_preferences?: any;
  timezone?: string;
}

export interface StudentProfile {
  user_id: number;
  program_name: string;
  program_type: string;
  start_date: string;
  expected_end_date: string;
  actual_end_date?: string;
  supervisor_id?: number;
  co_supervisor_id?: number;
  status: string;
  research_area?: string;
  thesis_title?: string;
  tags?: string[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export type LoginCredentials = LoginRequest;

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  role?: UserRole;
}