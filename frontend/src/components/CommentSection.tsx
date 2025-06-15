'use client';

import React, { useState } from 'react';
import { MessageSquarePlus } from 'lucide-react';
import apiService from '@/services/api';

interface Comment {
  id: number;
  body: string;
  author_id: number;
  created_at: string;
  votes: number;
}

interface CommentSectionProps {
  questionId?: number;
  answerId?: number;
  comments: Comment[];
  onCommentsUpdated: () => void;
}

interface CommentItemProps {
  comment: Comment;
  onVote: (commentId: number) => void;
  userVoteStatuses: Record<number, boolean>;
  votingStates: Record<number, boolean>;
}

function CommentItem({ comment, onVote, userVoteStatuses, votingStates }: CommentItemProps) {
  const hasVoted = userVoteStatuses[comment.id] || false;
  const isVoting = votingStates[comment.id] || false;

  return (
    <li className="flex items-start space-x-3 py-3 border-b border-gray-100 last:border-b-0">
      {/* Comment actions - Vote section (horizontal layout like Stack Overflow) */}
      <div className="flex items-center space-x-2">
        {/* Vote score */}
        {comment.votes > 0 && (
          <div className="comment-score">
            <span 
              className={`text-xs font-medium ${
                comment.votes >= 10 ? 'text-orange-600' : 'text-gray-600'
              }`} 
              title="number of 'useful comment' votes received"
            >
              {comment.votes}
            </span>
          </div>
        )}
        
        {/* Upvote button */}
        <div className="comment-voting">
          <button
            onClick={() => onVote(comment.id)}
            disabled={isVoting}
            className={`p-1 transition-colors ${
              hasVoted 
                ? 'text-orange-600' 
                : 'text-gray-400 hover:text-gray-600'
            } ${isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
            title="This comment adds something useful to the post"
            aria-label="Upvote Comment"
          >
            {/* Stack Overflow's exact arrow SVG */}
            <svg aria-hidden="true" className="w-[18px] h-[18px]" width="18" height="18" viewBox="0 0 18 18">
              <path fill="currentColor" d="M1 12h16L9 4z"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Comment content - Right side */}
      <div className="flex-1 min-w-0">
        <div className="text-sm text-gray-700">
          <span className="comment-copy">{comment.body}</span>
          {' '}
          <span className="text-gray-500">–</span>
          {' '}
          <a href="#" className="text-blue-600 hover:text-blue-800 no-underline">
            User {comment.author_id}
          </a>
          {' '}
          <span className="text-xs text-gray-500">
            {new Date(comment.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
    </li>
  );
}

export default function CommentSection({ questionId, answerId, comments, onCommentsUpdated }: CommentSectionProps) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [userVoteStatuses, setUserVoteStatuses] = useState<Record<number, boolean>>({});
  const [votingStates, setVotingStates] = useState<Record<number, boolean>>({});

  // Load vote statuses when comments change
  React.useEffect(() => {
    const loadVoteStatuses = async () => {
      const userId = 1; // Mock user ID
      const statuses: Record<number, boolean> = {};
      
      for (const comment of comments) {
        try {
          const response = await apiService.getCommentVoteStatus(comment.id, userId);
          if (response.data) {
            statuses[comment.id] = response.data.has_voted;
          }
        } catch (error) {
          console.error('Error loading vote status for comment', comment.id, error);
        }
      }
      
      setUserVoteStatuses(statuses);
    };

    if (comments.length > 0) {
      loadVoteStatuses();
    }
  }, [comments]);

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newComment.trim().length < 15) {
      alert('Comments must be at least 15 characters long');
      return;
    }

    setIsSubmitting(true);
    
    try {
      const userId = 1; // Mock user ID
      const response = await apiService.createComment(userId, newComment.trim(), questionId, answerId);
      
      if (response.error) {
        console.error('Error creating comment:', response.error);
        alert('Failed to post comment. Please try again.');
      } else {
        setNewComment('');
        setShowAddForm(false);
        onCommentsUpdated();
      }
    } catch (error) {
      console.error('Error submitting comment:', error);
      alert('Failed to post comment. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleVoteComment = async (commentId: number) => {
    if (votingStates[commentId]) return; // Already voting

    setVotingStates(prev => ({ ...prev, [commentId]: true }));

    try {
      const userId = 1; // Mock user ID
      const response = await apiService.voteComment(commentId, userId);
      
      if (response.error) {
        console.error('Error voting on comment:', response.error);
      } else {
        // Toggle the vote status
        setUserVoteStatuses(prev => ({
          ...prev,
          [commentId]: !prev[commentId]
        }));
        
        // Refresh comments to get updated vote counts
        onCommentsUpdated();
      }
    } catch (error) {
      console.error('Error voting on comment:', error);
    } finally {
      setVotingStates(prev => ({ ...prev, [commentId]: false }));
    }
  };

  return (
    <div className="mt-6">
      {/* Comments list */}
      {comments.length > 0 && (
        <div className="border-t border-gray-200 pt-4">
          <div className="mb-4">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              {comments.length} Comment{comments.length !== 1 ? 's' : ''}
            </h3>
            {/* Use ul like Stack Overflow */}
            <ul className="list-none p-0 m-0">
              {comments.map((comment) => (
                <CommentItem
                  key={comment.id}
                  comment={comment}
                  onVote={handleVoteComment}
                  userVoteStatuses={userVoteStatuses}
                  votingStates={votingStates}
                />
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Add comment section */}
      <div className={`${comments.length > 0 ? 'border-t border-gray-200 pt-4' : 'mt-4'}`}>
        {!showAddForm ? (
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            <MessageSquarePlus className="w-4 h-4" />
            <span>Add a comment</span>
          </button>
        ) : (
          <form onSubmit={handleSubmitComment} className="space-y-3">
            <div>
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Use comments to ask for more information or suggest improvements. Avoid answering questions in comments."
                className="w-full p-3 border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                rows={3}
                minLength={15}
                maxLength={1000}
              />
              <div className="text-xs text-gray-500 mt-1">
                {newComment.length < 15 ? 
                  `Enter at least ${15 - newComment.length} more characters` : 
                  `${1000 - newComment.length} characters remaining`
                }
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                type="submit"
                disabled={newComment.trim().length < 15 || isSubmitting}
                className="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? 'Posting...' : 'Add Comment'}
              </button>
              
              <button
                type="button"
                onClick={() => {
                  setShowAddForm(false);
                  setNewComment('');
                }}
                className="px-4 py-2 text-gray-600 text-sm rounded-md hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
