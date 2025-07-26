import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { Login } from './pages/Login';
import { StudentDashboard } from './pages/StudentDashboard';
import { SupervisorDashboard } from './pages/SupervisorDashboard';
import { Reports } from './pages/Reports';
import { PhDPlanning } from './pages/PhDPlanning';
import { NotificationSettings } from './pages/NotificationSettings';
import { UserRole } from './types/auth';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            
            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              {/* Default redirect */}
              <Route index element={<Navigate to="/dashboard" replace />} />
              
              {/* Dashboard redirect based on role */}
              <Route path="dashboard" element={<DashboardRedirect />} />
              
              {/* Student routes */}
              <Route
                path="dashboard/student"
                element={
                  <ProtectedRoute allowedRoles={[UserRole.STUDENT]}>
                    <StudentDashboard />
                  </ProtectedRoute>
                }
              />
              
              {/* Supervisor routes */}
              <Route
                path="dashboard/supervisor"
                element={
                  <ProtectedRoute allowedRoles={[UserRole.SUPERVISOR, UserRole.ADMIN]}>
                    <SupervisorDashboard />
                  </ProtectedRoute>
                }
              />
              
              {/* Admin routes */}
              <Route
                path="dashboard/admin"
                element={
                  <ProtectedRoute allowedRoles={[UserRole.ADMIN, UserRole.SYSTEM_ADMIN]}>
                    <div className="p-8">
                      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
                      <p className="mt-2 text-gray-600">Coming soon...</p>
                    </div>
                  </ProtectedRoute>
                }
              />
              
              {/* Other routes - placeholders for now */}
              <Route 
                path="reports" 
                element={
                  <ProtectedRoute allowedRoles={[UserRole.STUDENT]}>
                    <Reports />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="phd-planning" 
                element={
                  <ProtectedRoute allowedRoles={[UserRole.STUDENT]}>
                    <PhDPlanning />
                  </ProtectedRoute>
                } 
              />
              <Route path="meetings" element={<div className="p-8">Meetings Page</div>} />
              <Route path="projects" element={<div className="p-8">Projects Page</div>} />
              <Route path="students" element={<div className="p-8">Students Page</div>} />
              <Route path="users" element={<div className="p-8">Users Management</div>} />
              <Route path="profile" element={<div className="p-8">Profile Page</div>} />
              <Route path="settings" element={<NotificationSettings />} />
              <Route path="notifications" element={<NotificationSettings />} />
              
              {/* 404 */}
              <Route path="*" element={<div className="p-8">404 - Page not found</div>} />
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
      <Toaster position="top-right" />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

// Dashboard redirect component
const DashboardRedirect: React.FC = () => {
  const { user } = useAuth();
  
  if (!user) return <Navigate to="/login" replace />;
  
  switch (user.role) {
    case UserRole.STUDENT:
      return <Navigate to="/dashboard/student" replace />;
    case UserRole.SUPERVISOR:
      return <Navigate to="/dashboard/supervisor" replace />;
    case UserRole.ADMIN:
    case UserRole.SYSTEM_ADMIN:
      return <Navigate to="/dashboard/admin" replace />;
    default:
      return <Navigate to="/login" replace />;
  }
};

export default App;