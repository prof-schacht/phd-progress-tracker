import React from 'react';

interface StatusBadgeProps {
  status: 'on_track' | 'at_risk' | 'needs_attention' | 'overdue' | 'submitted' | 'pending';
  size?: 'small' | 'medium' | 'large';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'medium' }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'on_track':
        return {
          label: 'On Track',
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          dotColor: 'bg-green-400',
        };
      case 'at_risk':
        return {
          label: 'At Risk',
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          dotColor: 'bg-yellow-400',
        };
      case 'needs_attention':
        return {
          label: 'Needs Attention',
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          dotColor: 'bg-red-400',
        };
      case 'overdue':
        return {
          label: 'Overdue',
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          dotColor: 'bg-red-400',
        };
      case 'submitted':
        return {
          label: 'Submitted',
          bgColor: 'bg-blue-100',
          textColor: 'text-blue-800',
          dotColor: 'bg-blue-400',
        };
      case 'pending':
        return {
          label: 'Pending',
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          dotColor: 'bg-gray-400',
        };
      default:
        return {
          label: status,
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          dotColor: 'bg-gray-400',
        };
    }
  };

  const sizeClasses = {
    small: 'text-xs px-2 py-0.5',
    medium: 'text-sm px-2.5 py-0.5',
    large: 'text-base px-3 py-1',
  };

  const config = getStatusConfig();

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full ${config.bgColor} ${config.textColor} ${sizeClasses[size]}`}
    >
      <span className={`w-1.5 h-1.5 mr-1.5 rounded-full ${config.dotColor}`}></span>
      {config.label}
    </span>
  );
};