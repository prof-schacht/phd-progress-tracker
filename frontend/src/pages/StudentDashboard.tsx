import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Calendar, 
  TrendingUp, 
  MessageSquare, 
  FileText,
  Zap,
  Target
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { dashboardApi } from '../api/dashboard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { DeadlineCountdown } from '../components/dashboard/DeadlineCountdown';
import { ProgressRing } from '../components/dashboard/ProgressRing';
import { formatDistanceToNow, parseISO } from 'date-fns';

export const StudentDashboard: React.FC = () => {
  const { user } = useAuth();

  const { data: currentPeriod, isLoading: periodLoading } = useQuery({
    queryKey: ['currentPeriod'],
    queryFn: dashboardApi.getCurrentPeriod,
    refetchInterval: 5 * 60 * 1000, // Refresh every 5 minutes
  });

  const { data: dashboardData, isLoading: dashboardLoading, error } = useQuery({
    queryKey: ['studentDashboard'],
    queryFn: dashboardApi.getStudentDashboard,
    refetchInterval: 5 * 60 * 1000, // Refresh every 5 minutes
  });

  if (periodLoading || dashboardLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <LoadingSpinner size="large" message="Loading dashboard..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center">
        <ErrorMessage 
          title="Failed to load dashboard" 
          message="Please try refreshing the page or contact support if the problem persists."
        />
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="flex h-screen items-center justify-center">
        <ErrorMessage 
          title="No dashboard data" 
          message="Unable to load your dashboard data."
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name}! 
          </h1>
          <div className="mt-2 flex items-center text-sm text-gray-600">
            <Zap className="mr-1 h-4 w-4 text-yellow-500" />
            <span className="font-medium">{dashboardData.stats?.currentStreak || 0} day streak</span>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Left Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Next Deadline */}
            {dashboardData.currentPeriod?.period && (
              <DeadlineCountdown
                title="Bi-weekly Update"
                dueDate={dashboardData.currentPeriod.period.endDate}
                onAction={() => window.location.href = '/reports/submit'}
              />
            )}

            {/* Research Pipeline */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Your Research Pipeline
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {dashboardData.researchProjects?.length > 0 ? (
                  dashboardData.researchProjects.map((project: any) => (
                    <div
                      key={project.id}
                      className="border rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <h3 className="font-medium text-gray-900">{project.title}</h3>
                      <div className="mt-3">
                        <ProgressRing
                          progress={project.progress || 0}
                          size={80}
                          strokeWidth={6}
                          showPercentage={true}
                        />
                      </div>
                      <p className="mt-2 text-xs text-gray-500 capitalize">
                        {project.status?.replace('_', ' ') || 'Unknown'}
                      </p>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500 col-span-3">No research projects yet</p>
                )}
              </div>
            </div>

            {/* Recent Progress */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Recent Progress
              </h2>
              <div className="space-y-3">
                {dashboardData.currentPeriod?.previousReport ? (
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="h-2 w-2 rounded-full bg-green-500 mt-2"></div>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-gray-900">
                        Last report submitted{' '}
                        {dashboardData.currentPeriod.previousReport.submittedAt ? 
                          formatDistanceToNow(parseISO(dashboardData.currentPeriod.previousReport.submittedAt), {
                            addSuffix: true,
                          }) : 'recently'}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {dashboardData.currentPeriod.previousReport.nextSteps?.substring(0, 100) || 'No details available'}...
                      </p>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No recent reports</p>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Stats & Quick Actions */}
          <div className="space-y-6">
            {/* Stats */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Your Stats
              </h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">On-time submissions</span>
                  <span className="text-2xl font-bold text-green-600">
                    {dashboardData.stats?.totalReports > 0 
                      ? Math.round((dashboardData.stats.onTimeSubmissions / dashboardData.stats.totalReports) * 100)
                      : 0}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Total reports</span>
                  <span className="text-2xl font-bold text-gray-900">
                    {dashboardData.stats?.totalReports || 0}
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Actions
              </h2>
              <div className="space-y-2">
                <button className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
                  <FileText className="mr-2 h-4 w-4" />
                  Submit Update
                </button>
                <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                  <Calendar className="mr-2 h-4 w-4" />
                  Schedule Meeting
                </button>
                <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                  <Target className="mr-2 h-4 w-4" />
                  View Milestones
                </button>
              </div>
            </div>

            {/* Recent Feedback */}
            {dashboardData.recentFeedback?.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Recent Feedback
                </h2>
                <div className="space-y-3">
                  {dashboardData.recentFeedback.map((feedback: any) => (
                    <div key={feedback.id} className="text-sm">
                      <p className="text-gray-900">{feedback.content}</p>
                      <p className="text-gray-500 mt-1">
                        — {feedback.author?.full_name || 'Unknown'}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};