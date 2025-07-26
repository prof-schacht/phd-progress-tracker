import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { FileText, Plus, Calendar, Clock } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { reportsApi } from '../services/reports';
import { dashboardApi } from '../services/dashboard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { ReportForm } from '../components/reports/ReportForm';
import { ReportsList } from '../components/reports/ReportsList';

export const Reports: React.FC = () => {
  const { user } = useAuth();
  const [showNewReport, setShowNewReport] = useState(false);
  const [selectedPeriodType, setSelectedPeriodType] = useState<'biweekly' | 'quarterly'>('biweekly');

  // Get current period info
  const { data: currentPeriod, isLoading: periodLoading, error: periodError } = useQuery({
    queryKey: ['currentPeriod'],
    queryFn: dashboardApi.getCurrentPeriod,
    enabled: user?.role === 'student',
  });

  // Get past reports
  const { data: reports, isLoading: reportsLoading, refetch } = useQuery({
    queryKey: ['reports', 'past'],
    queryFn: () => reportsApi.getReports({ status: 'submitted' }),
    enabled: user?.role === 'student',
  });

  if (periodLoading || reportsLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <LoadingSpinner size="large" message="Loading reports..." />
      </div>
    );
  }

  const canSubmitReport = currentPeriod?.period && !currentPeriod.current_report;
  const currentReportType = currentPeriod?.period?.period_type as 'biweekly' | 'quarterly';

  // Debug logging
  console.log('Current Period:', currentPeriod);
  console.log('Can Submit Report:', canSubmitReport);
  console.log('Period Error:', periodError);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
            <p className="mt-2 text-gray-600">
              Manage your bi-weekly updates and quarterly reviews
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedPeriodType('biweekly');
                setShowNewReport(true);
              }}
              className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
            >
              <Plus className="mr-2 h-4 w-4" />
              Submit Bi-weekly Report
            </button>
            <button
              onClick={() => {
                setSelectedPeriodType('quarterly');
                setShowNewReport(true);
              }}
              className="inline-flex items-center rounded-md bg-green-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500"
            >
              <Plus className="mr-2 h-4 w-4" />
              Submit Quarterly Review
            </button>
          </div>
        </div>
      </div>

      {/* Current Period Alert */}
      {currentPeriod?.period && (
        <div className={`mb-6 rounded-lg border p-4 ${
          canSubmitReport 
            ? 'border-yellow-400 bg-yellow-50' 
            : 'border-green-400 bg-green-50'
        }`}>
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {canSubmitReport ? (
                <Clock className="h-5 w-5 text-yellow-400" />
              ) : (
                <FileText className="h-5 w-5 text-green-400" />
              )}
            </div>
            <div className="ml-3 flex-1">
              <h3 className="text-sm font-medium text-gray-900">
                Current Period: {currentPeriod.period.period_type === 'biweekly' ? 'Bi-weekly' : 'Quarterly'} Report
              </h3>
              <div className="mt-1 text-sm text-gray-600">
                <p>
                  Period: {new Date(currentPeriod.period.start_date).toLocaleDateString()} - {' '}
                  {new Date(currentPeriod.period.end_date).toLocaleDateString()}
                </p>
                {canSubmitReport ? (
                  <p className="mt-1 font-medium text-yellow-700">
                    Report due by {new Date(currentPeriod.period.end_date).toLocaleDateString()}
                  </p>
                ) : (
                  <p className="mt-1 text-green-700">
                    Report submitted on {currentPeriod.current_report?.submitted_at && 
                      new Date(currentPeriod.current_report.submitted_at).toLocaleDateString()
                    }
                  </p>
                )}
              </div>
              {canSubmitReport && (
                <div className="mt-3">
                  <button
                    onClick={() => {
                      setSelectedPeriodType(currentReportType || 'biweekly');
                      setShowNewReport(true);
                    }}
                    className="inline-flex items-center rounded-md bg-yellow-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-yellow-500"
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Submit {currentPeriod.period.period_type === 'biweekly' ? 'Bi-weekly' : 'Quarterly'} Report
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Report Form Modal */}
      {showNewReport && (
        <ReportForm
          periodId={currentPeriod?.period?.id || 1} // Fallback period ID
          periodType={selectedPeriodType}
          previousReport={currentPeriod?.previousReport}
          onClose={() => setShowNewReport(false)}
          onSuccess={() => {
            setShowNewReport(false);
            refetch();
          }}
        />
      )}

      {/* Reports Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setSelectedPeriodType('biweekly')}
              className={`whitespace-nowrap border-b-2 py-2 px-1 text-sm font-medium ${
                selectedPeriodType === 'biweekly'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
              }`}
            >
              <Calendar className="inline-block h-4 w-4 mr-2" />
              Bi-weekly Reports
            </button>
            <button
              onClick={() => setSelectedPeriodType('quarterly')}
              className={`whitespace-nowrap border-b-2 py-2 px-1 text-sm font-medium ${
                selectedPeriodType === 'quarterly'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
              }`}
            >
              <FileText className="inline-block h-4 w-4 mr-2" />
              Quarterly Reviews
            </button>
          </nav>
        </div>
      </div>

      {/* Reports List */}
      <ReportsList 
        reportType={selectedPeriodType}
        reports={reports}
        onRefresh={refetch}
      />
    </div>
  );
};