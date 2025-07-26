import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { X, MessageSquare, Send, Eye, EyeOff, Download } from 'lucide-react';
import { reportsApi } from '../../services/reports';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';

interface ReportDetailProps {
  reportId: number;
  onClose: () => void;
  onUpdate: () => void;
}

export const ReportDetail: React.FC<ReportDetailProps> = ({ 
  reportId, 
  onClose,
  onUpdate 
}) => {
  const { user } = useAuth();
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState('');
  const [commentVisibility, setCommentVisibility] = useState<'public' | 'private' | 'supervisor_only'>('public');

  const { data: report, isLoading, error } = useQuery({
    queryKey: ['report', reportId],
    queryFn: () => reportsApi.getReport(reportId),
  });

  const commentMutation = useMutation({
    mutationFn: () => reportsApi.addComment(reportId, {
      content: comment,
      visibility: commentVisibility,
    }),
    onSuccess: () => {
      setComment('');
      setShowComment(false);
      onUpdate();
    },
  });

  if (isLoading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-500 bg-opacity-75">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-500 bg-opacity-75">
        <div className="bg-white p-6 rounded-lg">
          <ErrorMessage message="Failed to load report details" />
          <button onClick={onClose} className="mt-4 text-sm text-blue-600 hover:text-blue-800">
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={onClose} />
        
        <div className="relative w-full max-w-4xl rounded-lg bg-white shadow-xl">
          <div className="flex items-center justify-between border-b px-6 py-4">
            <div>
              <h2 className="text-xl font-semibold">Report Details</h2>
              <p className="text-sm text-gray-500">
                {new Date(report.period.start_date).toLocaleDateString()} - {' '}
                {new Date(report.period.end_date).toLocaleDateString()}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <button className="text-gray-400 hover:text-gray-500">
                <Download className="h-5 w-5" />
              </button>
              <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
                <X className="h-6 w-6" />
              </button>
            </div>
          </div>

          <div className="max-h-[70vh] overflow-y-auto p-6">
            {/* Report Content */}
            <div className="space-y-6">
              <div>
                <h3 className="text-sm font-medium text-gray-700">Accomplishments</h3>
                <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                  {report.accomplishments || 'No accomplishments recorded.'}
                </p>
              </div>

              {report.blockers && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Blockers/Challenges</h3>
                  <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                    {report.blockers}
                  </p>
                </div>
              )}

              <div>
                <h3 className="text-sm font-medium text-gray-700">Plans for Next Period</h3>
                <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                  {report.next_period_plan || 'No plans recorded.'}
                </p>
              </div>

              {/* Time Allocation */}
              {report.time_allocation && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Time Allocation</h3>
                  <div className="mt-2 space-y-2">
                    {Object.entries(report.time_allocation).map(([key, value]) => {
                      const labels = {
                        research: 'Research Work',
                        writing: 'Writing & Documentation',
                        teaching: 'Teaching Activities',
                        meetings: 'Meetings & Supervision',
                        commercial_projects: 'Commercial Projects',
                        other: 'Other Activities'
                      };
                      
                      return (
                        <div key={key} className="flex items-center">
                          <span className="w-40 text-sm text-gray-600">
                            {labels[key as keyof typeof labels] || key}:
                          </span>
                          <div className="flex-1 mx-3">
                            <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-blue-500"
                                style={{ width: `${value}%` }}
                              />
                            </div>
                          </div>
                          <span className="text-sm text-gray-600 w-10">{value}%</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Quarterly Fields */}
              {report.quarterly_achievements && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Quarterly Achievements</h3>
                  <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                    {report.quarterly_achievements}
                  </p>
                </div>
              )}

              {report.challenges && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Major Challenges</h3>
                  <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                    {report.challenges}
                  </p>
                </div>
              )}

              {report.goals_next_quarter && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Goals for Next Quarter</h3>
                  <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                    {report.goals_next_quarter}
                  </p>
                </div>
              )}

              {report.training_completed && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Training Completed</h3>
                  <p className="mt-2 text-sm text-gray-900 whitespace-pre-wrap">
                    {report.training_completed}
                  </p>
                </div>
              )}

              {/* Comments Section */}
              <div className="border-t pt-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium text-gray-700">Comments</h3>
                  {user?.role === 'student' && (
                    <button
                      onClick={() => setShowComment(!showComment)}
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      <MessageSquare className="inline-block h-4 w-4 mr-1" />
                      Add Comment
                    </button>
                  )}
                </div>

                {showComment && (
                  <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      placeholder="Add your comment..."
                      className="w-full rounded-md border-gray-300 text-sm"
                      rows={3}
                    />
                    <div className="mt-2 flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <select
                          value={commentVisibility}
                          onChange={(e) => setCommentVisibility(e.target.value as any)}
                          className="text-sm rounded-md border-gray-300"
                        >
                          <option value="public">Public</option>
                          <option value="private">Private</option>
                          <option value="supervisor_only">Supervisor Only</option>
                        </select>
                        <span className="text-xs text-gray-500">
                          {commentVisibility === 'private' && <EyeOff className="inline h-3 w-3" />}
                          {commentVisibility === 'public' && <Eye className="inline h-3 w-3" />}
                        </span>
                      </div>
                      <button
                        onClick={() => commentMutation.mutate()}
                        disabled={!comment.trim() || commentMutation.isPending}
                        className="inline-flex items-center rounded-md bg-blue-600 px-3 py-1 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
                      >
                        <Send className="mr-1 h-3 w-3" />
                        Send
                      </button>
                    </div>
                  </div>
                )}

                {/* Comments List */}
                {report.comments && report.comments.length > 0 ? (
                  <div className="space-y-3">
                    {report.comments.map((comment: any) => (
                      <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
                        <div className="flex items-start justify-between">
                          <div>
                            <p className="text-sm font-medium text-gray-900">
                              {comment.author.full_name}
                            </p>
                            <p className="text-xs text-gray-500">
                              {new Date(comment.created_at).toLocaleString()}
                            </p>
                          </div>
                          <span className="text-xs text-gray-500">
                            {comment.visibility === 'private' && <EyeOff className="h-3 w-3" />}
                          </span>
                        </div>
                        <p className="mt-2 text-sm text-gray-700">{comment.content}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No comments yet.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};