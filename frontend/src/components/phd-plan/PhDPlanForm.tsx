import { useState, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from '../../contexts/AuthContext';
import { phdPlanApi } from '../../services/phd-plan';
import { PhDPlan, PhDPlanUpdate, PlannedPaper, VenueRating, VenueType } from '../../types/phd-plan';
import { toast } from 'react-hot-toast';
import { Plus, Trash2, Save, AlertCircle } from 'lucide-react';

interface PhDPlanFormProps {
  plan: PhDPlan;
  onSuccess: () => void;
}

export function PhDPlanForm({ plan, onSuccess }: PhDPlanFormProps) {
  const { user } = useAuth();
  const initialData = {
    research_topic: plan.research_topic || '',
    research_question: plan.research_question || '',
    research_field: plan.research_field || '',
    expected_duration_years: plan.expected_duration_years || 4,
    proposal_text: plan.proposal_text || '',
    expose_text: plan.expose_text || '',
    papers: plan.papers.length === 3 ? plan.papers : [
      { paper_number: 1, title: '', research_question: '', venue_rating: VenueRating.B, target_completion_date: '' },
      { paper_number: 2, title: '', research_question: '', venue_rating: VenueRating.B, target_completion_date: '' },
      { paper_number: 3, title: '', research_question: '', venue_rating: VenueRating.B, target_completion_date: '' },
    ],
    change_reason: '',
  };
  
  const [formData, setFormData] = useState<PhDPlanUpdate>(initialData);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isDirty, setIsDirty] = useState(false);

  // Check if form data has changed from initial data
  useEffect(() => {
    const hasChanges = JSON.stringify(formData) !== JSON.stringify(initialData);
    setIsDirty(hasChanges);
  }, [formData]);

  // Warn user if they try to leave with unsaved changes
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = '';
      }
    };
    
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [isDirty]);

  const updateMutation = useMutation({
    mutationFn: (data: PhDPlanUpdate) => phdPlanApi.updatePhDPlan(user!.id, data),
    onSuccess: () => {
      toast.success('PhD plan updated successfully');
      setIsDirty(false);
      onSuccess();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update PhD plan');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    const newErrors: Record<string, string> = {};
    
    if (!formData.research_topic || formData.research_topic.length < 5) {
      newErrors.research_topic = 'Research topic must be at least 5 characters';
    }
    if (!formData.research_question || formData.research_question.length < 20) {
      newErrors.research_question = 'Research question must be at least 20 characters';
    }
    
    formData.papers?.forEach((paper, index) => {
      if (!paper.title || paper.title.length < 5) {
        newErrors[`paper_${index}_title`] = 'Paper title must be at least 5 characters';
      }
      if (!paper.research_question || paper.research_question.length < 10) {
        newErrors[`paper_${index}_question`] = 'Paper research question must be at least 10 characters';
      }
      if (!paper.target_completion_date) {
        newErrors[`paper_${index}_date`] = 'Target completion date is required';
      }
    });
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    updateMutation.mutate(formData);
  };

  const updatePaper = (index: number, field: keyof PlannedPaper, value: any) => {
    const newPapers = [...(formData.papers || [])];
    newPapers[index] = { ...newPapers[index], [field]: value };
    setFormData({ ...formData, papers: newPapers });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Basic Information */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Research Overview</h3>
        
        <div className="grid grid-cols-1 gap-6">
          <div>
            <label htmlFor="research_topic" className="block text-sm font-medium text-gray-700">
              Research Topic <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="research_topic"
              value={formData.research_topic}
              onChange={(e) => {
                setFormData({ ...formData, research_topic: e.target.value });
                setErrors({ ...errors, research_topic: '' });
              }}
              className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
                errors.research_topic 
                  ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
              }`}
              placeholder="e.g., Machine Learning for Healthcare Diagnostics"
            />
            {errors.research_topic && (
              <p className="mt-1 text-sm text-red-600">{errors.research_topic}</p>
            )}
          </div>

          <div>
            <label htmlFor="research_question" className="block text-sm font-medium text-gray-700">
              Main Research Question <span className="text-red-500">*</span>
            </label>
            <textarea
              id="research_question"
              rows={3}
              value={formData.research_question}
              onChange={(e) => {
                setFormData({ ...formData, research_question: e.target.value });
                setErrors({ ...errors, research_question: '' });
              }}
              className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
                errors.research_question 
                  ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
              }`}
              placeholder="What is the main question your PhD research aims to answer?"
            />
            {errors.research_question && (
              <p className="mt-1 text-sm text-red-600">{errors.research_question}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              {formData.research_question?.length || 0} characters (min 20)
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="research_field" className="block text-sm font-medium text-gray-700">
                Research Field
              </label>
              <input
                type="text"
                id="research_field"
                value={formData.research_field}
                onChange={(e) => setFormData({ ...formData, research_field: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                placeholder="e.g., Computer Science, AI"
              />
            </div>

            <div>
              <label htmlFor="expected_duration_years" className="block text-sm font-medium text-gray-700">
                Expected Duration (years)
              </label>
              <select
                id="expected_duration_years"
                value={formData.expected_duration_years}
                onChange={(e) => setFormData({ ...formData, expected_duration_years: parseInt(e.target.value) })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              >
                {[3, 4, 5, 6, 7].map((year) => (
                  <option key={year} value={year}>{year} years</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Proposal & Exposé */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Proposal & Exposé</h3>
        
        <div className="space-y-4">
          <div>
            <label htmlFor="proposal_text" className="block text-sm font-medium text-gray-700">
              Proposal Summary
            </label>
            <textarea
              id="proposal_text"
              rows={4}
              value={formData.proposal_text}
              onChange={(e) => setFormData({ ...formData, proposal_text: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Provide a summary of your research proposal..."
            />
            <p className="mt-1 text-xs text-gray-500">
              You can also upload a PDF document after saving
            </p>
          </div>

          <div>
            <label htmlFor="expose_text" className="block text-sm font-medium text-gray-700">
              Exposé Summary
            </label>
            <textarea
              id="expose_text"
              rows={4}
              value={formData.expose_text}
              onChange={(e) => setFormData({ ...formData, expose_text: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Provide a summary of your exposé..."
            />
            <p className="mt-1 text-xs text-gray-500">
              You can also upload a PDF document after saving
            </p>
          </div>
        </div>
      </div>

      {/* Planned Papers */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Planned Papers (3 Required)</h3>
        
        <div className="space-y-6">
          {formData.papers?.map((paper, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-3">Paper {index + 1}</h4>
              
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Title <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={paper.title}
                    onChange={(e) => {
                      updatePaper(index, 'title', e.target.value);
                      setErrors({ ...errors, [`paper_${index}_title`]: '' });
                    }}
                    className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
                      errors[`paper_${index}_title`] 
                        ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                    }`}
                    placeholder="Paper title"
                  />
                  {errors[`paper_${index}_title`] && (
                    <p className="mt-1 text-sm text-red-600">{errors[`paper_${index}_title`]}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Research Question <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    rows={2}
                    value={paper.research_question}
                    onChange={(e) => {
                      updatePaper(index, 'research_question', e.target.value);
                      setErrors({ ...errors, [`paper_${index}_question`]: '' });
                    }}
                    className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
                      errors[`paper_${index}_question`] 
                        ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                    }`}
                    placeholder="What specific question will this paper address?"
                  />
                  {errors[`paper_${index}_question`] && (
                    <p className="mt-1 text-sm text-red-600">{errors[`paper_${index}_question`]}</p>
                  )}
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Venue Type
                    </label>
                    <select
                      value={paper.venue_type || ''}
                      onChange={(e) => updatePaper(index, 'venue_type', e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="">Select type</option>
                      <option value={VenueType.CONFERENCE}>Conference</option>
                      <option value={VenueType.JOURNAL}>Journal</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Venue Rating <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={paper.venue_rating}
                      onChange={(e) => updatePaper(index, 'venue_rating', e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value={VenueRating.A_STAR}>A*</option>
                      <option value={VenueRating.A}>A</option>
                      <option value={VenueRating.B}>B</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Target Date <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="date"
                      value={paper.target_completion_date}
                      onChange={(e) => {
                        updatePaper(index, 'target_completion_date', e.target.value);
                        setErrors({ ...errors, [`paper_${index}_date`]: '' });
                      }}
                      className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
                        errors[`paper_${index}_date`] 
                          ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                          : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                      }`}
                    />
                    {errors[`paper_${index}_date`] && (
                      <p className="mt-1 text-sm text-red-600">{errors[`paper_${index}_date`]}</p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Target Venue
                  </label>
                  <input
                    type="text"
                    value={paper.target_venue || ''}
                    onChange={(e) => updatePaper(index, 'target_venue', e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="e.g., ICML, NeurIPS, Nature Machine Intelligence"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <div className="flex">
            <AlertCircle className="h-5 w-5 text-blue-400 flex-shrink-0" />
            <div className="ml-3">
              <p className="text-sm text-blue-700">
                Each paper will automatically create a milestone with the target completion date.
                Papers must target venues rated B or higher.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Change Reason */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label htmlFor="change_reason" className="block text-sm font-medium text-gray-700">
          Reason for Changes
        </label>
        <textarea
          id="change_reason"
          rows={2}
          value={formData.change_reason}
          onChange={(e) => setFormData({ ...formData, change_reason: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="Briefly describe why you're making these changes..."
        />
      </div>

      {/* Submit Button */}
      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onSuccess}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={updateMutation.isPending || !isDirty}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          <Save className="mr-2 h-4 w-4" />
          {updateMutation.isPending ? 'Saving...' : isDirty ? 'Save Changes' : 'No Changes'}
        </button>
      </div>
    </form>
  );
}