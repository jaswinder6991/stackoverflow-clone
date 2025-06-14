'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import apiService from '../services/api';

export default function QuestionForm() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [filteredTags, setFilteredTags] = useState<string[]>([]);
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // Use default tags directly instead of trying to fetch from API
    const defaultTags = ['javascript', 'python', 'react', 'node.js', 'html', 'css', 'typescript', 'java', 'c#', 'php'];
    setAvailableTags(defaultTags);
    console.log('Using default tags:', defaultTags);
  }, []);

  // Filter available tags based on user input
  useEffect(() => {
    if (tagInput.trim()) {
      const filtered = availableTags.filter(tag => 
        tag.toLowerCase().includes(tagInput.toLowerCase())
      );
      setFilteredTags(filtered.slice(0, 5)); // Show top 5 matching tags
    } else {
      setFilteredTags([]);
    }
  }, [tagInput, availableTags]);

  const handleAddTag = (tag: string) => {
    if (!tags.includes(tag) && tags.length < 5) {
      setTags([...tags, tag]);
      setTagInput('');
      setFilteredTags([]);
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleTagInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      if (filteredTags.length > 0) {
        // Add the first suggestion
        handleAddTag(filteredTags[0]);
      } else if (tagInput.trim().length >= 2) {
        // Add as new tag if at least 2 characters
        handleAddTag(tagInput.trim().toLowerCase());
      }
    } else if (e.key === 'Backspace' && tagInput === '' && tags.length > 0) {
      // Remove the last tag when pressing backspace in an empty input
      handleRemoveTag(tags[tags.length - 1]);
    }
  };
  
  // Add a custom tag function
  const addCustomTag = () => {
    if (tagInput.trim().length >= 2 && !tags.includes(tagInput.trim().toLowerCase()) && tags.length < 5) {
      handleAddTag(tagInput.trim().toLowerCase());
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError('Please provide a title for your question');
      return;
    }

    if (!body.trim()) {
      setError('Please provide details in the body of your question');
      return;
    }

    if (tags.length === 0) {
      setError('Please add at least one tag to your question');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // For now, using a dummy user_id since auth is commented out
      // In a real implementation, this would come from the auth context
      const dummyUserId = 1;
      
      const questionData = {
        title: title,
        body: body,  // Now our API expects body directly
        tags: tags,
        author_id: dummyUserId
      };
      
      console.log('Submitting question:', questionData);
      
      const response = await apiService.createQuestion(questionData);
      
      console.log('Submit response:', response);

      if (response.error) {
        console.error('Submit failed:', response.error);
        setError(response.error || 'Failed to post question. Please try again.');
      } else {
        console.log('Question posted successfully');
        setSuccess(true);
        
        // Redirect to the new question
        if (response.data && typeof response.data === 'object' && 'id' in response.data) {
          setTimeout(() => {
            router.push(`/questions/${(response.data as {id: number}).id}`);
          }, 1000);
        } else {
          // If we don't have the ID, redirect to questions list
          setTimeout(() => {
            router.push('/questions');
          }, 1000);
        }
      }
    } catch (err) {
      console.error('Error submitting question:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Ask a public question</h1>
      
      <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-6">
        <h3 className="font-semibold text-blue-800 mb-2">Writing a good question</h3>
        <p className="text-blue-700 text-sm">
          You&apos;re ready to ask a programming-related question and this form will help guide you through the process.
          Looking to ask a non-programming question? See the topics here to find a relevant site.
        </p>
        <ul className="text-blue-700 text-sm list-disc ml-5 mt-2">
          <li>Summarize your problem in a one-line title</li>
          <li>Describe your problem in more detail</li>
          <li>Describe what you tried and what you expected to happen</li>
          <li>Add "tags" which help surface your question to members of the community</li>
          <li>Review your question and post it to the site</li>
        </ul>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded text-green-700">
          Your question has been posted successfully! Redirecting...
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6 bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium text-gray-700" htmlFor="question-title">
              Title
              <span className="text-red-500 ml-1">*</span>
            </label>
            <span className="text-xs text-gray-500">{title.length}/150</span>
          </div>
          <p className="text-sm text-gray-600 mb-2">
            Be specific and imagine you&apos;re asking a question to another person.
          </p>
          <input
            id="question-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Is there an R function for finding the index of an element in a vector?"
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            maxLength={150}
            required
            disabled={isSubmitting}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="question-body">
            Body
            <span className="text-red-500 ml-1">*</span>
          </label>
          <p className="text-sm text-gray-600 mb-2">
            Include all the information someone would need to answer your question. Minimum 20 characters.
          </p>
          <div className="border border-gray-300 rounded overflow-hidden">
            <div className="bg-gray-50 px-3 py-2 border-b border-gray-300 flex items-center space-x-2">
              <button type="button" className="px-2 py-1 hover:bg-gray-200 rounded text-sm font-bold">B</button>
              <button type="button" className="px-2 py-1 hover:bg-gray-200 rounded text-sm italic">I</button>
              <button type="button" className="px-2 py-1 hover:bg-gray-200 rounded text-sm font-mono">Code</button>
              <button type="button" className="px-2 py-1 hover:bg-gray-200 rounded text-sm">Link</button>
              <button type="button" className="px-2 py-1 hover:bg-gray-200 rounded text-sm">Image</button>
            </div>
            <textarea
              id="question-body"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="Enter your question details here..."
              className="w-full px-3 py-2 min-h-[200px] resize-y focus:outline-none focus:border-blue-500"
              required
              minLength={20}
              disabled={isSubmitting}
            />
          </div>
          <div className="text-xs text-gray-500 mt-2">
            Format using: **bold**, *italic*, `code`, [link text](url), &gt; blockquote, - list item
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="question-tags">
            Tags
            <span className="text-red-500 ml-1">*</span>
          </label>
          <p className="text-sm text-gray-600 mb-2">
            Add up to 5 tags to describe what your question is about. Start typing to see suggestions.
          </p>
          <div className="flex flex-wrap items-center gap-2 px-3 py-2 border border-gray-300 rounded focus-within:border-blue-500">
            {tags.map(tag => (
              <div 
                key={tag} 
                className="px-2 py-1 bg-blue-100 text-blue-800 rounded-md flex items-center gap-1"
              >
                <span>{tag}</span>
                <button 
                  type="button" 
                  onClick={() => handleRemoveTag(tag)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  &times;
                </button>
              </div>
            ))}
            <input
              id="question-tags"
              type="text"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={handleTagInputKeyDown}
              placeholder={tags.length === 0 ? "e.g. (javascript react node.js)" : ""}
              className="flex-grow px-1 py-1 focus:outline-none"
              disabled={isSubmitting || tags.length >= 5}
            />
          </div>
          {filteredTags.length > 0 && (
            <div className="mt-1 bg-white border border-gray-300 rounded shadow-sm">
              {filteredTags.map(tag => (
                <div 
                  key={tag}
                  onClick={() => handleAddTag(tag)}
                  className="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                >
                  {tag}
                </div>
              ))}
            </div>
          )}
          {tags.length >= 5 && (
            <p className="text-xs text-orange-600 mt-1">
              You've reached the maximum of 5 tags.
            </p>
          )}
        </div>

        <div className="flex items-center space-x-4 pt-4">
          <button
            type="submit"
            disabled={isSubmitting || !title.trim() || !body.trim() || tags.length === 0}
            className={`px-6 py-2 rounded font-medium ${
              isSubmitting || !title.trim() || !body.trim() || tags.length === 0
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isSubmitting ? 'Posting...' : 'Post your question'}
          </button>
          
          <button
            type="button"
            onClick={() => {
              if (confirm('Are you sure you want to discard this question?')) {
                router.push('/');
              }
            }}
            className="text-gray-600 hover:text-gray-800 px-6 py-2 border border-gray-300 rounded hover:bg-gray-50"
            disabled={isSubmitting}
          >
            Discard
          </button>
        </div>
      </form>
    </div>
  );
}
