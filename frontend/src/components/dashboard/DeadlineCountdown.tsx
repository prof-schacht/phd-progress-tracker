import React from 'react';
import { Clock, AlertTriangle } from 'lucide-react';
import { formatDistanceToNow, parseISO, differenceInDays } from 'date-fns';

interface DeadlineCountdownProps {
  title: string;
  dueDate: string;
  onAction?: () => void;
  actionLabel?: string;
}

export const DeadlineCountdown: React.FC<DeadlineCountdownProps> = ({
  title,
  dueDate,
  onAction,
  actionLabel = 'Submit',
}) => {
  const date = parseISO(dueDate);
  const daysRemaining = differenceInDays(date, new Date());
  const isOverdue = daysRemaining < 0;
  const isUrgent = daysRemaining <= 3 && daysRemaining >= 0;

  const getColorClasses = () => {
    if (isOverdue) return 'bg-red-50 border-red-200 text-red-900';
    if (isUrgent) return 'bg-yellow-50 border-yellow-200 text-yellow-900';
    return 'bg-blue-50 border-blue-200 text-blue-900';
  };

  const getIconColorClasses = () => {
    if (isOverdue) return 'text-red-500';
    if (isUrgent) return 'text-yellow-500';
    return 'text-blue-500';
  };

  return (
    <div className={`rounded-lg border-2 p-6 ${getColorClasses()}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{title}</h3>
          <div className="mt-2 flex items-center">
            {isOverdue ? (
              <AlertTriangle className={`h-5 w-5 mr-2 ${getIconColorClasses()}`} />
            ) : (
              <Clock className={`h-5 w-5 mr-2 ${getIconColorClasses()}`} />
            )}
            <span className="text-2xl font-bold">
              {isOverdue ? 'Overdue by' : ''} {formatDistanceToNow(date, { addSuffix: !isOverdue })}
            </span>
          </div>
        </div>
        {onAction && (
          <button
            onClick={onAction}
            className={`ml-4 px-4 py-2 rounded-md font-medium transition-colors ${
              isOverdue
                ? 'bg-red-600 text-white hover:bg-red-700'
                : isUrgent
                ? 'bg-yellow-600 text-white hover:bg-yellow-700'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {actionLabel}
          </button>
        )}
      </div>
    </div>
  );
};