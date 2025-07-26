import React, { useState, useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Bell, X, Check, AlertCircle, Info, Calendar, MessageSquare } from 'lucide-react';
import { formatDistanceToNow, parseISO } from 'date-fns';
import { notificationsApi } from '../../api/notifications';
import { NotificationType } from '../../types/notifications';
import { LoadingSpinner } from '../common/LoadingSpinner';

export const NotificationDropdown: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fetch notifications
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['notifications', { limit: 10, unread_only: false }],
    queryFn: () => notificationsApi.getNotifications({ limit: 10 }),
    enabled: isOpen,
    refetchInterval: 30000, // Refresh every 30 seconds when open
  });

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationsApi.markAsRead(notificationId);
      refetch();
    } catch (error) {
      console.error('Failed to mark notification as read:', error);
    }
  };

  const getNotificationIcon = (type: NotificationType) => {
    switch (type) {
      case 'reminder':
        return <Calendar className="h-5 w-5 text-blue-500" />;
      case 'alert':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'feedback':
        return <MessageSquare className="h-5 w-5 text-green-500" />;
      case 'announcement':
        return <Info className="h-5 w-5 text-purple-500" />;
      default:
        return <Bell className="h-5 w-5 text-gray-500" />;
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Bell Icon Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <span className="sr-only">View notifications</span>
        <Bell className="h-6 w-6" />
        
        {/* Unread count badge */}
        {data?.unread_count && data.unread_count > 0 && (
          <span className="absolute top-0 right-0 block h-2 w-2 transform translate-x-1/2 -translate-y-1/2 rounded-full bg-red-500 ring-2 ring-white" />
        )}
      </button>

      {/* Dropdown Panel */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-96 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Notifications</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-500"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            {data?.unread_count && data.unread_count > 0 && (
              <p className="mt-1 text-sm text-gray-500">
                {data.unread_count} unread notification{data.unread_count > 1 ? 's' : ''}
              </p>
            )}
          </div>

          <div className="max-h-96 overflow-y-auto">
            {isLoading ? (
              <div className="p-8 text-center">
                <LoadingSpinner size="medium" />
              </div>
            ) : data?.items.length === 0 ? (
              <div className="p-8 text-center">
                <Bell className="mx-auto h-12 w-12 text-gray-300" />
                <p className="mt-2 text-sm text-gray-500">No notifications yet</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {data?.items.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 hover:bg-gray-50 transition-colors ${
                      !notification.read_at ? 'bg-blue-50' : ''
                    }`}
                  >
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="ml-3 flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {notification.subject}
                        </p>
                        <p className="mt-1 text-sm text-gray-500">
                          {notification.content}
                        </p>
                        <div className="mt-2 flex items-center justify-between">
                          <p className="text-xs text-gray-400">
                            {formatDistanceToNow(parseISO(notification.created_at), {
                              addSuffix: true,
                            })}
                          </p>
                          {!notification.read_at && (
                            <button
                              onClick={() => handleMarkAsRead(notification.id)}
                              className="text-xs text-blue-600 hover:text-blue-800 flex items-center"
                            >
                              <Check className="h-3 w-3 mr-1" />
                              Mark as read
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="p-4 border-t border-gray-200 flex justify-between">
            <a
              href="/notifications"
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              onClick={() => setIsOpen(false)}
            >
              View all
            </a>
            <a
              href="/settings"
              className="text-sm text-gray-600 hover:text-gray-800"
              onClick={() => setIsOpen(false)}
            >
              Settings
            </a>
          </div>
        </div>
      )}
    </div>
  );
};