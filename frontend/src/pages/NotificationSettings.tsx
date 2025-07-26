import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Bell, Mail, MessageSquare, Clock, Check } from 'lucide-react';
import { notificationsApi } from '../api/notifications';
import { NotificationPreferences, EmailFrequency } from '../types/notifications';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import toast from 'react-hot-toast';

export const NotificationSettings: React.FC = () => {
  const [testEmailSent, setTestEmailSent] = useState(false);

  // Fetch current preferences
  const { data: preferences, isLoading, error, refetch } = useQuery({
    queryKey: ['notificationPreferences'],
    queryFn: notificationsApi.getPreferences,
  });

  // Update preferences mutation
  const updateMutation = useMutation({
    mutationFn: notificationsApi.updatePreferences,
    onSuccess: () => {
      toast.success('Notification preferences updated successfully');
      refetch();
    },
    onError: () => {
      toast.error('Failed to update preferences');
    },
  });

  // Send test notification mutation
  const testMutation = useMutation({
    mutationFn: notificationsApi.sendTest,
    onSuccess: () => {
      setTestEmailSent(true);
      toast.success('Test email sent! Check your inbox.');
      setTimeout(() => setTestEmailSent(false), 5000);
    },
    onError: () => {
      toast.error('Failed to send test email');
    },
  });

  const handleToggle = (field: keyof NotificationPreferences, value: boolean) => {
    if (preferences) {
      updateMutation.mutate({ [field]: value });
    }
  };

  const handleFrequencyChange = (frequency: EmailFrequency) => {
    if (preferences) {
      updateMutation.mutate({ email_frequency: frequency });
    }
  };

  const handleQuietHoursChange = (start: string, end: string) => {
    if (preferences) {
      updateMutation.mutate({ quiet_hours: { start, end } });
    }
  };

  const handleTimezoneChange = (timezone: string) => {
    if (preferences) {
      updateMutation.mutate({ timezone });
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <LoadingSpinner size="large" message="Loading preferences..." />
      </div>
    );
  }

  if (error || !preferences) {
    return (
      <div className="flex h-screen items-center justify-center">
        <ErrorMessage 
          title="Failed to load preferences" 
          message="Please try refreshing the page."
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Notification Settings</h1>
          <p className="mt-2 text-sm text-gray-600">
            Manage how and when you receive notifications from PhD Progress Tracker
          </p>
        </div>

        {/* Email Notifications */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900 flex items-center">
                  <Mail className="h-5 w-5 mr-2 text-gray-400" />
                  Email Notifications
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  Receive important updates and reminders via email
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('email_enabled', !preferences.email_enabled)}
                className={`
                  relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent 
                  transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                  ${preferences.email_enabled ? 'bg-blue-600' : 'bg-gray-200'}
                `}
              >
                <span
                  className={`
                    pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 
                    transition duration-200 ease-in-out
                    ${preferences.email_enabled ? 'translate-x-5' : 'translate-x-0'}
                  `}
                />
              </button>
            </div>

            {preferences.email_enabled && (
              <div className="mt-6 space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700">Email Frequency</label>
                  <div className="mt-2 space-y-2">
                    {(['immediate', 'daily_digest', 'weekly_digest'] as EmailFrequency[]).map((freq) => (
                      <label key={freq} className="flex items-center">
                        <input
                          type="radio"
                          name="email_frequency"
                          value={freq}
                          checked={preferences.email_frequency === freq}
                          onChange={() => handleFrequencyChange(freq)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                        />
                        <span className="ml-3 text-sm text-gray-700">
                          {freq === 'immediate' && 'Send immediately'}
                          {freq === 'daily_digest' && 'Daily digest'}
                          {freq === 'weekly_digest' && 'Weekly digest'}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <button
                    onClick={() => testMutation.mutate()}
                    disabled={testMutation.isPending || testEmailSent}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {testEmailSent ? (
                      <>
                        <Check className="h-4 w-4 mr-2 text-green-500" />
                        Test email sent!
                      </>
                    ) : (
                      <>
                        <Mail className="h-4 w-4 mr-2" />
                        Send test email
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Quiet Hours */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 flex items-center">
              <Clock className="h-5 w-5 mr-2 text-gray-400" />
              Quiet Hours
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Set times when you don't want to receive notifications
            </p>

            <div className="mt-4 grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="quiet-start" className="block text-sm font-medium text-gray-700">
                  Start time
                </label>
                <input
                  type="time"
                  id="quiet-start"
                  value={preferences.quiet_hours?.start || '22:00'}
                  onChange={(e) => handleQuietHoursChange(
                    e.target.value,
                    preferences.quiet_hours?.end || '08:00'
                  )}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label htmlFor="quiet-end" className="block text-sm font-medium text-gray-700">
                  End time
                </label>
                <input
                  type="time"
                  id="quiet-end"
                  value={preferences.quiet_hours?.end || '08:00'}
                  onChange={(e) => handleQuietHoursChange(
                    preferences.quiet_hours?.start || '22:00',
                    e.target.value
                  )}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Timezone */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900">Timezone</h3>
            <p className="mt-1 text-sm text-gray-500">
              All notifications will be sent according to this timezone
            </p>

            <div className="mt-4">
              <select
                value={preferences.timezone}
                onChange={(e) => handleTimezoneChange(e.target.value)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              >
                <option value="Europe/Berlin">Berlin (GMT+1)</option>
                <option value="Europe/London">London (GMT)</option>
                <option value="America/New_York">New York (GMT-5)</option>
                <option value="America/Los_Angeles">Los Angeles (GMT-8)</option>
                <option value="Asia/Tokyo">Tokyo (GMT+9)</option>
                <option value="Australia/Sydney">Sydney (GMT+11)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Future Integrations */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 flex items-center">
              <MessageSquare className="h-5 w-5 mr-2 text-gray-400" />
              Other Channels
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Slack and Microsoft Teams integrations coming soon!
            </p>

            <div className="mt-4 space-y-3">
              <div className="flex items-center justify-between opacity-50">
                <div>
                  <p className="text-sm font-medium text-gray-700">Slack</p>
                  <p className="text-xs text-gray-500">Get notifications in your Slack workspace</p>
                </div>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Coming soon</span>
              </div>
              <div className="flex items-center justify-between opacity-50">
                <div>
                  <p className="text-sm font-medium text-gray-700">Microsoft Teams</p>
                  <p className="text-xs text-gray-500">Receive notifications in Teams channels</p>
                </div>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Coming soon</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};