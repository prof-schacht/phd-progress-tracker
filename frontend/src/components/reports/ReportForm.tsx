import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { X, Save, AlertCircle } from 'lucide-react';
import { reportsApi } from '../../services/reports';
import { ReportEntryCreate, TimeAllocation } from '../../types/report';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';

interface ReportFormProps {
  periodId: number;
  periodType: 'biweekly' | 'quarterly';
  previousReport?: any;
  onClose: () => void;
  onSuccess: () => void;
}

export const ReportForm: React.FC<ReportFormProps> = ({
  periodId,
  periodType,
  previousReport,
  onClose,
  onSuccess,
}) => {
  const [formData, setFormData] = useState<Partial<ReportEntryCreate>>({
    period_id: periodId,
    accomplishments: '',
    blockers: '',
    next_period_plan: previousReport?.nextSteps || '',
    time_allocation: {
      research: 30,
      writing: 20,
      teaching: 15,
      meetings: 10,
      commercial_projects: 15,
      other: 10,
    },
    tags: [],
    is_draft: false,
  });

  const [quarterlyData, setQuarterlyData] = useState({
    quarterly_achievements: '',
    challenges: '',
    goals_next_quarter: '',
    training_completed: '',
    wellbeing_note: '',
  });

  const submitMutation = useMutation({
    mutationFn: (data: ReportEntryCreate) => reportsApi.submitReport(data),
    onSuccess: () => {
      onSuccess();
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const submitData: ReportEntryCreate = {
      ...formData,
      ...(periodType === 'quarterly' ? quarterlyData : {}),
    } as ReportEntryCreate;

    submitMutation.mutate(submitData);
  };

  const updateTimeAllocation = (field: keyof TimeAllocation, value: number) => {
    setFormData(prev => ({
      ...prev,
      time_allocation: {
        ...prev.time_allocation!,
        [field]: value,
      },
    }));
  };

  const totalTimeAllocation = Object.values(formData.time_allocation || {}).reduce((a, b) => a + b, 0);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={onClose} />
        
        <div className="relative w-full max-w-4xl rounded-lg bg-white shadow-xl">
          <div className="flex items-center justify-between border-b px-6 py-4">
            <h2 className="text-xl font-semibold">
              Submit {periodType === 'quarterly' ? 'Quarterly' : 'Bi-weekly'} Report
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-500"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="p-6">
            {submitMutation.isError && (
              <ErrorMessage 
                message={
                  submitMutation.error?.response?.data?.detail?.[0]?.msg || 
                  "Failed to submit report. Please ensure all fields meet minimum requirements (10+ characters)."
                } 
              />
            )}

            {previousReport?.nextSteps && (
              <div className="mb-4 rounded-md bg-blue-50 p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-blue-400" />
                  <div className="ml-3">
                    <p className="text-sm text-blue-800">
                      Auto-populated from your previous report's "Next Steps"
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Bi-weekly Fields */}
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  What did you accomplish this period? *
                  <span className={`ml-2 text-xs ${formData.accomplishments.length < 10 ? 'text-red-600' : 'text-gray-500'}`}>
                    ({formData.accomplishments.length} characters, min 10)
                  </span>
                </label>
                <textarea
                  required
                  rows={4}
                  value={formData.accomplishments}
                  onChange={(e) => setFormData({ ...formData, accomplishments: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                  placeholder="List your key accomplishments... (minimum 10 characters)"
                  minLength={10}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Any blockers or challenges?
                </label>
                <textarea
                  rows={3}
                  value={formData.blockers}
                  onChange={(e) => setFormData({ ...formData, blockers: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                  placeholder="Describe any obstacles you faced..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  What are your plans for next period? *
                  <span className={`ml-2 text-xs ${formData.next_period_plan.length < 10 ? 'text-red-600' : 'text-gray-500'}`}>
                    ({formData.next_period_plan.length} characters, min 10)
                  </span>
                </label>
                <textarea
                  required
                  rows={3}
                  value={formData.next_period_plan}
                  onChange={(e) => setFormData({ ...formData, next_period_plan: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                  placeholder="Outline your goals for the next period... (minimum 10 characters)"
                  minLength={10}
                />
              </div>

              {/* Time Allocation */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Allocation (%) {totalTimeAllocation !== 100 && (
                    <span className="text-red-600 ml-2">Must total 100%</span>
                  )}
                </label>
                <div className="grid grid-cols-1 gap-3">
                  {Object.entries(formData.time_allocation || {}).map(([key, value]) => {
                    const labels = {
                      research: 'Research Work',
                      writing: 'Writing & Documentation',
                      teaching: 'Teaching Activities',
                      meetings: 'Meetings & Supervision',
                      commercial_projects: 'Commercial Projects',
                      other: 'Other Activities'
                    };
                    
                    return (
                      <div key={key} className="flex items-center justify-between">
                        <label className="text-sm font-medium text-gray-700 flex-1">
                          {labels[key as keyof typeof labels] || key}:
                        </label>
                        <div className="flex items-center">
                          <input
                            type="number"
                            min="0"
                            max="100"
                            value={value}
                            onChange={(e) => updateTimeAllocation(key as keyof TimeAllocation, parseInt(e.target.value) || 0)}
                            className="w-16 rounded-md border-gray-300 border-2 text-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-2 py-1 font-medium"
                          />
                          <span className="ml-2 text-sm text-gray-500">%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Quarterly Additional Fields */}
              {periodType === 'quarterly' && (
                <>
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium mb-4">Quarterly Review Details</h3>
                    
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700">
                          Key Achievements This Quarter
                        </label>
                        <textarea
                          rows={3}
                          value={quarterlyData.quarterly_achievements}
                          onChange={(e) => setQuarterlyData({ ...quarterlyData, quarterly_achievements: e.target.value })}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700">
                          Major Challenges Faced
                        </label>
                        <textarea
                          rows={3}
                          value={quarterlyData.challenges}
                          onChange={(e) => setQuarterlyData({ ...quarterlyData, challenges: e.target.value })}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700">
                          Goals for Next Quarter
                        </label>
                        <textarea
                          rows={3}
                          value={quarterlyData.goals_next_quarter}
                          onChange={(e) => setQuarterlyData({ ...quarterlyData, goals_next_quarter: e.target.value })}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700">
                          Training/Workshops Completed
                        </label>
                        <textarea
                          rows={2}
                          value={quarterlyData.training_completed}
                          onChange={(e) => setQuarterlyData({ ...quarterlyData, training_completed: e.target.value })}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700">
                          Wellbeing Note (Private)
                        </label>
                        <textarea
                          rows={2}
                          value={quarterlyData.wellbeing_note}
                          onChange={(e) => setQuarterlyData({ ...quarterlyData, wellbeing_note: e.target.value })}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white text-gray-900 px-3 py-2"
                          placeholder="This will only be visible to you..."
                        />
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitMutation.isPending || totalTimeAllocation !== 100}
                className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {submitMutation.isPending ? (
                  <>
                    <LoadingSpinner size="small" />
                    <span className="ml-2">Submitting...</span>
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Submit Report
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};