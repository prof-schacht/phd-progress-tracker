import { PhDPlan, VenueType } from '../../types/phd-plan';
import { Calendar, FileText, Target, Award, Clock, User } from 'lucide-react';
import { format } from 'date-fns';

interface PhDPlanViewProps {
  plan: PhDPlan;
}

export function PhDPlanView({ plan }: PhDPlanViewProps) {
  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Research Overview</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-500">Research Topic</label>
            <p className="mt-1 text-sm text-gray-900">{plan.research_topic || 'Not specified'}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500">Main Research Question</label>
            <p className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
              {plan.research_question || 'Not specified'}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-500">Research Field</label>
              <p className="mt-1 text-sm text-gray-900">{plan.research_field || 'Not specified'}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Expected Duration</label>
              <p className="mt-1 text-sm text-gray-900">{plan.expected_duration_years} years</p>
            </div>
          </div>
        </div>
      </div>

      {/* Proposal & Exposé */}
      {(plan.proposal_text || plan.expose_text || plan.proposal_document_id || plan.expose_document_id) && (
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Proposal & Exposé</h3>
          
          <div className="space-y-4">
            {plan.proposal_text && (
              <div>
                <label className="block text-sm font-medium text-gray-500">Proposal Summary</label>
                <p className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{plan.proposal_text}</p>
              </div>
            )}

            {plan.expose_text && (
              <div>
                <label className="block text-sm font-medium text-gray-500">Exposé Summary</label>
                <p className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{plan.expose_text}</p>
              </div>
            )}

            <div className="flex space-x-4">
              {plan.proposal_document_id && (
                <div className="flex items-center text-sm text-blue-600">
                  <FileText className="h-4 w-4 mr-1" />
                  <span>Proposal document uploaded</span>
                </div>
              )}
              {plan.expose_document_id && (
                <div className="flex items-center text-sm text-blue-600">
                  <FileText className="h-4 w-4 mr-1" />
                  <span>Exposé document uploaded</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Planned Papers */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Planned Papers</h3>
        
        <div className="space-y-4">
          {plan.papers.map((paper, index) => (
            <div key={paper.id || index} className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center">
                    <Target className="h-5 w-5 text-gray-400 mr-2" />
                    <h4 className="text-base font-medium text-gray-900">
                      Paper {paper.paper_number}: {paper.title}
                    </h4>
                  </div>
                  
                  <div className="mt-3 space-y-2">
                    <div>
                      <label className="text-xs font-medium text-gray-500">Research Question</label>
                      <p className="text-sm text-gray-700">{paper.research_question}</p>
                    </div>

                    {paper.methodology && (
                      <div>
                        <label className="text-xs font-medium text-gray-500">Methodology</label>
                        <p className="text-sm text-gray-700">{paper.methodology}</p>
                      </div>
                    )}

                    {paper.expected_contribution && (
                      <div>
                        <label className="text-xs font-medium text-gray-500">Expected Contribution</label>
                        <p className="text-sm text-gray-700">{paper.expected_contribution}</p>
                      </div>
                    )}

                    <div className="flex flex-wrap gap-4 mt-3 text-sm">
                      <div className="flex items-center text-gray-600">
                        <Calendar className="h-4 w-4 mr-1" />
                        <span>Target: {format(new Date(paper.target_completion_date), 'MMM yyyy')}</span>
                      </div>
                      
                      {paper.target_venue && (
                        <div className="flex items-center text-gray-600">
                          <Award className="h-4 w-4 mr-1" />
                          <span>{paper.target_venue}</span>
                        </div>
                      )}

                      <div className="flex items-center space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          paper.venue_type === VenueType.JOURNAL
                            ? 'bg-purple-100 text-purple-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {paper.venue_type || 'TBD'}
                        </span>
                        
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          paper.venue_rating === 'A*'
                            ? 'bg-green-100 text-green-800'
                            : paper.venue_rating === 'A'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {paper.venue_rating} Rating
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metadata */}
      <div className="text-sm text-gray-500 space-y-1">
        <div className="flex items-center">
          <Clock className="h-4 w-4 mr-1" />
          <span>Created: {format(new Date(plan.created_at), 'PPP')}</span>
        </div>
        {plan.updated_at && (
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>Last updated: {format(new Date(plan.updated_at), 'PPP')}</span>
          </div>
        )}
        {plan.submitted_at && (
          <div className="flex items-center">
            <User className="h-4 w-4 mr-1" />
            <span>Submitted: {format(new Date(plan.submitted_at), 'PPP')}</span>
          </div>
        )}
        {plan.approved_at && (
          <div className="flex items-center">
            <User className="h-4 w-4 mr-1" />
            <span>Approved: {format(new Date(plan.approved_at), 'PPP')}</span>
          </div>
        )}
      </div>
    </div>
  );
}