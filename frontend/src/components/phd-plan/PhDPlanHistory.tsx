import { useQuery } from '@tanstack/react-query';
import { phdPlanApi } from '../../services/phd-plan';
import { format } from 'date-fns';
import { Clock, User, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

interface PhDPlanHistoryProps {
  planId: number;
}

export function PhDPlanHistory({ planId }: PhDPlanHistoryProps) {
  const [expandedVersions, setExpandedVersions] = useState<Set<number>>(new Set());

  const { data: versions, isLoading, error } = useQuery({
    queryKey: ['phd-plan-history', planId],
    queryFn: () => phdPlanApi.getPhDPlanHistory(planId),
  });

  const toggleVersion = (versionId: number) => {
    const newExpanded = new Set(expandedVersions);
    if (newExpanded.has(versionId)) {
      newExpanded.delete(versionId);
    } else {
      newExpanded.add(versionId);
    }
    setExpandedVersions(newExpanded);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        <p className="font-semibold">Error loading version history</p>
      </div>
    );
  }

  if (!versions || versions.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <FileText className="mx-auto h-12 w-12 text-gray-300 mb-3" />
        <p>No version history available yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600 mb-4">
        Track all changes made to your PhD plan over time. Each version represents a snapshot of your plan at that point.
      </p>

      {versions.map((version) => (
        <div key={version.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <button
            onClick={() => toggleVersion(version.id)}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-600">
                <Clock className="h-4 w-4 mr-1" />
                <span>{format(new Date(version.created_at), 'PPP')}</span>
              </div>
              <div className="text-sm font-medium text-gray-900">
                Version {version.version_number}
              </div>
              {version.change_reason && (
                <div className="text-sm text-gray-600 italic">
                  "{version.change_reason}"
                </div>
              )}
            </div>
            {expandedVersions.has(version.id) ? (
              <ChevronUp className="h-5 w-5 text-gray-400" />
            ) : (
              <ChevronDown className="h-5 w-5 text-gray-400" />
            )}
          </button>

          {expandedVersions.has(version.id) && (
            <div className="px-4 py-3 border-t border-gray-200 bg-gray-50">
              {version.changes_made && Object.keys(version.changes_made).length > 0 ? (
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Changes in this version:</h4>
                  {Object.entries(version.changes_made).map(([field, change]: [string, any]) => {
                    // Special handling for paper changes
                    if (field === 'papers') {
                      return (
                        <div key={field} className="text-sm">
                          <span className="font-medium text-gray-700 block mb-2">Papers:</span>
                          <div className="ml-4 space-y-2">
                            {Object.entries(change).map(([paperKey, paperChange]: [string, any]) => (
                              <div key={paperKey} className="border-l-2 border-gray-200 pl-3">
                                <div className="font-medium text-gray-600">
                                  Paper {paperKey.replace('paper_', '')}
                                </div>
                                {paperChange.action === 'modified' && paperChange.changes && (
                                  <div className="ml-2 mt-1 space-y-1">
                                    {Object.entries(paperChange.changes).map(([fieldName, fieldChange]: [string, any]) => (
                                      <div key={fieldName} className="text-xs">
                                        <span className="text-gray-500">
                                          {fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                                        </span>
                                        {fieldChange.old && (
                                          <span className="text-red-600 line-through ml-1">
                                            {fieldChange.old}
                                          </span>
                                        )}
                                        <span className="text-green-600 ml-1">
                                          → {fieldChange.new}
                                        </span>
                                      </div>
                                    ))}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      );
                    }
                    
                    // Regular field changes
                    return (
                      <div key={field} className="text-sm">
                        <span className="font-medium text-gray-700">
                          {field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                        </span>
                        <div className="mt-1 space-y-1">
                          {change.old && (
                            <div className="text-red-600 line-through">
                              {typeof change.old === 'string' ? change.old : JSON.stringify(change.old)}
                            </div>
                          )}
                          <div className="text-green-600">
                            {typeof change.new === 'string' ? change.new : JSON.stringify(change.new)}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="space-y-3">
                  <h4 className="text-sm font-medium text-gray-700">Full snapshot:</h4>
                  
                  <div>
                    <label className="text-xs font-medium text-gray-500">Research Topic</label>
                    <p className="text-sm text-gray-700">
                      {version.data_snapshot.research_topic || <span className="italic text-gray-400">Not provided</span>}
                    </p>
                  </div>

                  <div>
                    <label className="text-xs font-medium text-gray-500">Research Question</label>
                    <p className="text-sm text-gray-700">
                      {version.data_snapshot.research_question || <span className="italic text-gray-400">Not provided</span>}
                    </p>
                  </div>

                  {version.data_snapshot.research_field && (
                    <div>
                      <label className="text-xs font-medium text-gray-500">Research Field</label>
                      <p className="text-sm text-gray-700">{version.data_snapshot.research_field}</p>
                    </div>
                  )}

                  {version.data_snapshot.expected_duration_years && (
                    <div>
                      <label className="text-xs font-medium text-gray-500">Expected Duration</label>
                      <p className="text-sm text-gray-700">{version.data_snapshot.expected_duration_years} years</p>
                    </div>
                  )}

                  {version.data_snapshot.proposal_text && (
                    <div>
                      <label className="text-xs font-medium text-gray-500">Proposal Text</label>
                      <p className="text-sm text-gray-700">{version.data_snapshot.proposal_text}</p>
                    </div>
                  )}

                  {version.data_snapshot.expose_text && (
                    <div>
                      <label className="text-xs font-medium text-gray-500">Exposé Text</label>
                      <p className="text-sm text-gray-700">{version.data_snapshot.expose_text}</p>
                    </div>
                  )}

                  {version.data_snapshot.papers && version.data_snapshot.papers.length > 0 && (
                    <div>
                      <label className="text-xs font-medium text-gray-500">Papers</label>
                      <div className="mt-1 space-y-2">
                        {version.data_snapshot.papers.map((paper: any, idx: number) => (
                          <div key={idx} className="text-sm text-gray-700">
                            Paper {paper.paper_number}: {paper.title}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}