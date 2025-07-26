import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../contexts/AuthContext';
import { phdPlanApi } from '../services/phd-plan';
import { PhDPlanForm } from '../components/phd-plan/PhDPlanForm';
import { PhDPlanView } from '../components/phd-plan/PhDPlanView';
import { PhDPlanHistory } from '../components/phd-plan/PhDPlanHistory';
import { PhDPlanStatus } from '../types/phd-plan';
import { toast } from 'react-hot-toast';
import { FileText, History, Edit3, Send, AlertCircle } from 'lucide-react';

export function PhDPlanning() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'overview' | 'edit' | 'history'>('overview');
  const [showSubmitDialog, setShowSubmitDialog] = useState(false);

  const { data: phdPlan, isLoading, error } = useQuery({
    queryKey: ['phd-plan', user?.id],
    queryFn: () => phdPlanApi.getPhDPlan(user!.id),
    enabled: !!user,
  });

  const submitMutation = useMutation({
    mutationFn: () => phdPlanApi.submitPhDPlan(user!.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['phd-plan'] });
      toast.success('PhD plan submitted for approval');
      setShowSubmitDialog(false);
      setActiveTab('overview');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to submit PhD plan');
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        <p className="font-semibold">Error loading PhD plan</p>
        <p className="text-sm mt-1">Please try refreshing the page.</p>
      </div>
    );
  }

  const canEdit = phdPlan && [PhDPlanStatus.DRAFT, PhDPlanStatus.REVISION_REQUESTED].includes(phdPlan.status);
  const canSubmit = phdPlan && phdPlan.status === PhDPlanStatus.DRAFT && phdPlan.papers.length === 3;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">PhD Planning</h1>
        <p className="mt-2 text-gray-600">
          Plan your PhD journey by defining your research topic, questions, and paper milestones.
        </p>
      </div>

      {/* Status Banner */}
      {phdPlan && (
        <div className={`mb-6 p-4 rounded-lg ${
          phdPlan.status === PhDPlanStatus.APPROVED 
            ? 'bg-green-50 border border-green-200' 
            : phdPlan.status === PhDPlanStatus.REVISION_REQUESTED
            ? 'bg-yellow-50 border border-yellow-200'
            : phdPlan.status === PhDPlanStatus.SUBMITTED
            ? 'bg-blue-50 border border-blue-200'
            : 'bg-gray-50 border border-gray-200'
        }`}>
          <div className="flex items-start">
            <AlertCircle className="h-5 w-5 mt-0.5 mr-2 flex-shrink-0" />
            <div>
              <p className="font-semibold">
                Status: {phdPlan.status.replace(/_/g, ' ').toUpperCase()}
              </p>
              {phdPlan.status === PhDPlanStatus.REVISION_REQUESTED && (
                <p className="text-sm mt-1">
                  Your supervisor has requested revisions. Please review their feedback and update your plan.
                </p>
              )}
              {phdPlan.status === PhDPlanStatus.SUBMITTED && (
                <p className="text-sm mt-1">
                  Your plan has been submitted and is awaiting supervisor approval.
                </p>
              )}
              {phdPlan.status === PhDPlanStatus.APPROVED && (
                <p className="text-sm mt-1">
                  Your plan has been approved! Paper milestones have been created automatically.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white shadow-sm rounded-lg">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-6 py-3 text-sm font-medium ${
                activeTab === 'overview'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <FileText className="inline-block w-4 h-4 mr-2" />
              Overview
            </button>
            {canEdit && (
              <button
                onClick={() => setActiveTab('edit')}
                className={`px-6 py-3 text-sm font-medium ${
                  activeTab === 'edit'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Edit3 className="inline-block w-4 h-4 mr-2" />
                Edit Plan
              </button>
            )}
            <button
              onClick={() => setActiveTab('history')}
              className={`px-6 py-3 text-sm font-medium ${
                activeTab === 'history'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <History className="inline-block w-4 h-4 mr-2" />
              History
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && phdPlan && (
            <>
              <PhDPlanView plan={phdPlan} />
              {canSubmit && (
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setShowSubmitDialog(true)}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <Send className="mr-2 h-4 w-4" />
                    Submit for Approval
                  </button>
                </div>
              )}
            </>
          )}

          {activeTab === 'edit' && phdPlan && canEdit && (
            <PhDPlanForm 
              plan={phdPlan} 
              onSuccess={() => {
                setActiveTab('overview');
                queryClient.invalidateQueries({ queryKey: ['phd-plan'] });
                queryClient.invalidateQueries({ queryKey: ['phd-plan-history', phdPlan.id] });
              }}
            />
          )}

          {activeTab === 'history' && phdPlan && (
            <PhDPlanHistory planId={phdPlan.id} />
          )}
        </div>
      </div>

      {/* Submit Confirmation Dialog */}
      {showSubmitDialog && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowSubmitDialog(false)} />
            
            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                    <Send className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <h3 className="text-base font-semibold leading-6 text-gray-900">
                      Submit PhD Plan for Approval
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        Are you sure you want to submit your PhD plan for approval? Once submitted, you won't be able to make changes until your supervisor reviews it.
                      </p>
                      <p className="text-sm text-gray-500 mt-2">
                        This will automatically create milestones for each of your planned papers.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button
                  type="button"
                  onClick={() => submitMutation.mutate()}
                  disabled={submitMutation.isPending}
                  className="inline-flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 sm:ml-3 sm:w-auto disabled:opacity-50"
                >
                  {submitMutation.isPending ? 'Submitting...' : 'Submit for Approval'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowSubmitDialog(false)}
                  className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}