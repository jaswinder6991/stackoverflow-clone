'use client';

import React, { useState } from 'react';
import apiService from '../services/api';

interface AnswerFormProps {
  questionId: number;
  onAnswerSubmitted?: (answerData: { question_id: number; user_id: number; body: string }) => Promise<{ success: boolean; error?: string }>;
}

export default function AnswerForm({ questionId, onAnswerSubmitted }: AnswerFormProps) {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim()) {
      setError('Please provide your answer content');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // For now, using a dummy user_id since auth is commented out
      // In a real implementation, this would come from the auth context
      const dummyUserId = 1;
      
      const answerData = {
        question_id: questionId,
        user_id: dummyUserId,
        body: content
      };
      
      console.log('Submitting answer for question:', questionId);
      console.log('Answer data:', answerData);
      
      let response;
      
      if (onAnswerSubmitted) {
        // Use the parent component's custom submit handler
        response = await onAnswerSubmitted(answerData);
      } else {
        // Use the default API service
        const apiResponse = await apiService.createAnswer(answerData);
        response = apiResponse.error ? { success: false, error: apiResponse.error } : { success: true };
      }

      console.log('Submit response:', response);

      if (!response.success) {
        console.error('Submit failed:', response.error);
        setError(response.error || 'Failed to post answer. Please try again.');
      } else {
        console.log('Answer posted successfully');
        setSuccess(true);
        setContent('');
        setTimeout(() => setSuccess(false), 3000);
      }
    } catch (err) {
      console.error('Error submitting answer:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="border-t border-gray-200 pt-6 mt-8">
      <h2 className="text-xl font-semibold mb-4">Your Answer</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded text-green-700">
          Your answer has been posted successfully!
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your answer here..."
            className="w-full h-40 p-3 border border-gray-300 rounded resize-vertical focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isSubmitting}
          />
        </div>
        
        <div className="mb-4 text-sm text-gray-600">
          <p className="mb-2">Thanks for contributing an answer to Stack Overflow!</p>
          <ul className="list-disc ml-6 space-y-1">
            <li>Please be sure to <strong>answer the question</strong>. Provide details and share your research!</li>
          </ul>
          <p className="mt-2">But <strong>avoid</strong> …</p>
          <ul className="list-disc ml-6 space-y-1">
            <li>Asking for help, clarification, or responding to other answers.</li>
            <li>Making statements based on opinion; back them up with references or personal experience.</li>
          </ul>
        </div>

        <div className="flex items-center space-x-4">
          <button
            type="submit"
            disabled={isSubmitting || !content.trim()}
            className={`px-6 py-2 rounded font-medium ${
              isSubmitting || !content.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isSubmitting ? 'Posting...' : 'Post Your Answer'}
          </button>
          
          <button
            type="button"
            onClick={() => setContent('')}
            className="text-gray-600 hover:text-gray-800"
            disabled={isSubmitting}
          >
            Discard
          </button>
        </div>
      </form>
    </div>
  );
}
