import React, { useState } from 'react';
import { Calendar, ChevronRight, FileText, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { ReportPeriod } from '../../types/report';
import { ReportDetail } from './ReportDetail';

interface ReportsListProps {
  reportType: 'biweekly' | 'quarterly';
  reports?: ReportPeriod[];
  onRefresh: () => void;
}

export const ReportsList: React.FC<ReportsListProps> = ({ 
  reportType, 
  reports = [],
  onRefresh 
}) => {
  const [selectedReportId, setSelectedReportId] = useState<number | null>(null);

  const filteredReports = reports.filter(
    report => report.period_type.toLowerCase() === reportType
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'SUBMITTED':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'REVIEWED':
        return <CheckCircle className="h-5 w-5 text-blue-500" />;
      case 'OVERDUE':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'SUBMITTED':
        return 'bg-green-100 text-green-800';
      case 'REVIEWED':
        return 'bg-blue-100 text-blue-800';
      case 'OVERDUE':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  if (filteredReports.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No reports yet</h3>
        <p className="mt-1 text-sm text-gray-500">
          You haven't submitted any {reportType} reports.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="overflow-hidden bg-white shadow sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {filteredReports.map((report) => (
            <li key={report.id}>
              <button
                onClick={() => setSelectedReportId(report.id)}
                className="block w-full px-4 py-4 hover:bg-gray-50 sm:px-6 text-left"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {getStatusIcon(report.status)}
                    <div className="ml-4">
                      <div className="flex items-center">
                        <p className="text-sm font-medium text-gray-900">
                          {reportType === 'quarterly' ? 'Q' : 'Period'} {' '}
                          {new Date(report.start_date).toLocaleDateString()} - {' '}
                          {new Date(report.end_date).toLocaleDateString()}
                        </p>
                        <span className={`ml-2 inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                          getStatusColor(report.status)
                        }`}>
                          {report.status}
                        </span>
                      </div>
                      <div className="mt-1 flex items-center text-sm text-gray-500">
                        <Calendar className="mr-1 h-4 w-4" />
                        Due: {new Date(report.due_date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <ChevronRight className="h-5 w-5 text-gray-400" />
                </div>
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* Report Detail Modal */}
      {selectedReportId && (
        <ReportDetail
          reportId={selectedReportId}
          onClose={() => setSelectedReportId(null)}
          onUpdate={onRefresh}
        />
      )}
    </>
  );
};