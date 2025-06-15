'use client';

import React, { useState, useEffect } from 'react';
import { ArrowUp, ArrowDown, Bookmark, Clock, CheckCircle, Loader2 } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';
import AnswerForm from './AnswerForm';
import CommentSection from './CommentSection';
import apiService from '@/services/api';

interface QuestionDetailProps {
  questionId: number;
}

interface BackendQuestion {
  id: number;
  title: string;
  body: string;
  author_id: number;
  created_at: string;
  updated_at: string;
  votes: number;
  views: number;
  is_answered: boolean;
}

interface UserVotesResponse {
  question_vote: 'up' | 'down' | null;
  answer_votes: Record<string, 'up' | 'down'>;
}

interface ApiQuestion {
  id: number;
  title: string;
  content: string;
  author: {
    id: number;
    name: string;
    email: string;
    reputation: number;
    avatar: string;
    location: string;
    website: string;
    is_active: boolean;
  };
  votes: number;
  views: number;
  asked: string;
  modified?: string;
  tags: string[];
  answers: ApiAnswer[];
}

interface ApiAnswer {
  id: number;
  body: string;
  question_id: number;
  author_id: number;
  created_at: string;
  updated_at: string;
  votes: number;
  is_accepted: boolean;
}

export default function QuestionDetail({ questionId }: QuestionDetailProps) {
  const [question, setQuestion] = useState<ApiQuestion | null>(null);
  const [answers, setAnswers] = useState<ApiAnswer[]>([]);
  const [questionComments, setQuestionComments] = useState<any[]>([]);
  const [answerComments, setAnswerComments] = useState<Record<number, any[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [votingStates, setVotingStates] = useState<{
    question?: { isVoting: boolean; userVote?: 'up' | 'down' | null };
    answers: Record<number, { isVoting: boolean; userVote?: 'up' | 'down' | null }>;
  }>({ answers: {} });

  // Fetch question data
  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        // Validate that questionId is a valid number
        if (isNaN(questionId) || !Number.isInteger(questionId)) {
          setError('Invalid question ID');
          setLoading(false);
          return;
        }
        
        setLoading(true);
        setError(null);
        
        // Mock user ID for now - in a real app this would come from auth context
        const userId = 1;
        
        // Fetch user's existing votes on this question and its answers
        try {
          const userVotesResponse = await apiService.getUserVotesOnQuestion(questionId, userId);
          if (userVotesResponse.data) {
            const votesData = userVotesResponse.data as UserVotesResponse;
            const { question_vote, answer_votes } = votesData;
            
            // Set initial voting states based on existing votes
            setVotingStates(prev => ({
              question: { 
                isVoting: false, 
                userVote: question_vote === 'up' ? 'up' : question_vote === 'down' ? 'down' : null 
              },
              answers: Object.keys(answer_votes).reduce((acc, answerId) => {
                const vote = answer_votes[parseInt(answerId)];
                acc[parseInt(answerId)] = {
                  isVoting: false,
                  userVote: vote === 'up' ? 'up' : vote === 'down' ? 'down' : null
                };
                return acc;
              }, {} as Record<number, { isVoting: boolean; userVote?: 'up' | 'down' | null }>)
            }));
          }
        } catch (voteError) {
          console.log('Could not fetch user votes (user may not be logged in):', voteError);
          // Initialize with empty voting states
          setVotingStates({ answers: {} });
        }
        
        // For now, let's fetch answers directly since we know that endpoint works
        const answersResponse = await fetch(`http://localhost:8000/answers/?question_id=${questionId}`);
        
        if (answersResponse.ok) {
          const answersData = await answersResponse.json();
          setAnswers(answersData);
          console.log('Fetched answers:', answersData);
          
          // Load comments for each answer
          const answerCommentsMap: Record<number, any[]> = {};
          for (const answer of answersData) {
            try {
              const commentsResponse = await apiService.getAnswerComments(answer.id);
              if (commentsResponse.data) {
                answerCommentsMap[answer.id] = commentsResponse.data;
              }
            } catch (error) {
              console.error(`Error loading comments for answer ${answer.id}:`, error);
              answerCommentsMap[answer.id] = [];
            }
          }
          setAnswerComments(answerCommentsMap);
        } else {
          console.error('Failed to fetch answers:', answersResponse.status);
        }

        // Try to fetch question (might fail, but we'll handle it)
        try {
          const questionResponse = await apiService.getQuestion(questionId);
          if (questionResponse.data) {
            // Convert backend question to frontend format
            const backendQuestion = questionResponse.data;
            const convertedQuestion: ApiQuestion = {
              id: backendQuestion.id,
              title: backendQuestion.title,
              content: backendQuestion.body,
              author: {
                id: backendQuestion.author_id,
                name: "User", // Default since backend doesn't return full
                email: "",
                reputation: 0,
                avatar: "",
                location: "",
                website: "",
                is_active: true
              },
              votes: backendQuestion.votes,
              views: backendQuestion.views,
              asked: backendQuestion.created_at,
              modified: backendQuestion.updated_at,
              tags: [], // Backend doesn't return tags in this response
              answers: answers // Use the answers we fetched separately
            };
            setQuestion(convertedQuestion);
            console.log('Fetched question:', convertedQuestion);
            
            // Load comments for the question
            try {
              const questionCommentsResponse = await apiService.getQuestionComments(questionId);
              if (questionCommentsResponse.data) {
                setQuestionComments(questionCommentsResponse.data);
              }
            } catch (error) {
              console.error('Error loading question comments:', error);
              setQuestionComments([]);
            }
          }
        } catch (questionError) {
          console.error('Failed to fetch question:', questionError);
          // Create a mock question for now
          setQuestion({
            id: questionId,
            title: "React hooks best practices",
            content: "What are the best practices for using React hooks?",
            author: {
              id: 1,
              name: "jane_smith",
              email: "jane@example.com",
              reputation: 150,
              avatar: "",
              location: "New York, NY",
              website: "https://janesmith.dev",
              is_active: true
            },
            votes: 0,
            views: 0,
            asked: new Date().toISOString(),
            tags: ["react"],
            answers: []
          });
        }
        
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load question data');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestion();
  }, [questionId]);

  // Comment refresh functions
  const refreshQuestionComments = async () => {
    try {
      const response = await apiService.getQuestionComments(questionId);
      if (response.data) {
        setQuestionComments(response.data);
      }
    } catch (error) {
      console.error('Error refreshing question comments:', error);
    }
  };

  const refreshAnswerComments = async (answerId: number) => {
    try {
      const response = await apiService.getAnswerComments(answerId);
      if (response.data) {
        setAnswerComments(prev => ({
          ...prev,
          [answerId]: response.data!
        }));
      }
    } catch (error) {
      console.error('Error refreshing answer comments:', error);
    }
  };

  // Voting handlers
  const handleQuestionVote = async (voteType: 'up' | 'down') => {
    if (!question) return;
    
    const currentVote = votingStates.question?.userVote;
    const isCurrentVote = currentVote === voteType;
    const newVote = isCurrentVote ? null : voteType;
    
    // Optimistic update
    setVotingStates(prev => ({
      ...prev,
      question: { isVoting: true, userVote: newVote }
    }));
    
    // Calculate vote delta based on Stack Overflow style voting
    // Each user can only have one vote, changing votes removes old and adds new
    let voteDelta = 0;
    if (isCurrentVote) {
      // Removing current vote
      voteDelta = voteType === 'up' ? -1 : 1;
    } else if (currentVote) {
      // Changing vote (e.g., from up to down)
      const removeOldVote = currentVote === 'up' ? -1 : 1;
      const addNewVote = voteType === 'up' ? 1 : -1;
      voteDelta = removeOldVote + addNewVote;
    } else {
      // Adding new vote
      voteDelta = voteType === 'up' ? 1 : -1;
    }
    
    // Update question votes optimistically
    setQuestion(prev => prev ? { ...prev, votes: prev.votes + voteDelta } : null);
    
    try {
      // Mock user ID for now
      const userId = 1;
      
      // If we're removing a vote, send the undo flag
      if (isCurrentVote) {
        // This means we're undoing a vote
        const response = await apiService.voteQuestion(question.id, userId, voteType, true);
        if (!response.error) {
          console.log('Question vote removed successfully');
        } else {
          // Revert optimistic update on error
          setQuestion(prev => prev ? { ...prev, votes: prev.votes - voteDelta } : null);
          console.error('Failed to remove vote from question:', response.error);
        }
      } else if (currentVote) {
        // We're changing vote type (e.g. from up to down)
        // First remove the old vote
        await apiService.voteQuestion(question.id, userId, currentVote, true);
        // Then add the new vote
        const response = await apiService.voteQuestion(question.id, userId, voteType);
        if (!response.error) {
          console.log('Question vote changed successfully');
        } else {
          // Revert optimistic update on error
          setQuestion(prev => prev ? { ...prev, votes: prev.votes - voteDelta } : null);
          console.error('Failed to change vote on question:', response.error);
        }
      } else {
        // We're adding a new vote
        const response = await apiService.voteQuestion(question.id, userId, voteType);
        if (!response.error) {
          console.log('Question vote recorded successfully');
        } else {
          // Revert optimistic update on error
          setQuestion(prev => prev ? { ...prev, votes: prev.votes - voteDelta } : null);
          console.error('Failed to vote on question:', response.error);
        }
      }
    } catch (error) {
      // Revert optimistic update on error
      setQuestion(prev => prev ? { ...prev, votes: prev.votes - voteDelta } : null);
      console.error('Error voting on question:', error);
    } finally {
      setVotingStates(prev => ({
        ...prev,
        question: { isVoting: false, userVote: newVote }
      }));
    }
  };

  const handleAnswerVote = async (answerId: number, voteType: 'up' | 'down') => {
    const currentVote = votingStates.answers[answerId]?.userVote;
    const isCurrentVote = currentVote === voteType;
    const newVote = isCurrentVote ? null : voteType;
    
    // Optimistic update
    setVotingStates(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [answerId]: { isVoting: true, userVote: newVote }
      }
    }));
    
    // Calculate vote delta based on Stack Overflow style voting
    // Each user can only have one vote, changing votes removes old and adds new
    let voteDelta = 0;
    if (isCurrentVote) {
      // Removing current vote
      voteDelta = voteType === 'up' ? -1 : 1;
    } else if (currentVote) {
      // Changing vote (e.g., from up to down)
      const removeOldVote = currentVote === 'up' ? -1 : 1;
      const addNewVote = voteType === 'up' ? 1 : -1;
      voteDelta = removeOldVote + addNewVote;
    } else {
      // Adding new vote
      voteDelta = voteType === 'up' ? 1 : -1;
    }
    
    // Update answer votes optimistically
    setAnswers(prev => prev.map(answer => 
      answer.id === answerId 
        ? { ...answer, votes: answer.votes + voteDelta }
        : answer
    ));
    
    try {
      // Mock user ID for now
      const userId = 1;
      
      // If we're removing a vote, send the undo flag
      if (isCurrentVote) {
        // This means we're undoing a vote
        const response = await apiService.voteAnswer(answerId, userId, voteType, true);
        if (!response.error) {
          console.log('Answer vote removed successfully');
        } else {
          // Revert optimistic update on error
          setAnswers(prev => prev.map(answer => 
            answer.id === answerId 
              ? { ...answer, votes: answer.votes - voteDelta }
              : answer
          ));
          console.error('Failed to remove vote from answer:', response.error);
        }
      } else if (currentVote) {
        // We're changing vote type (e.g. from up to down)
        // First remove the old vote
        await apiService.voteAnswer(answerId, userId, currentVote, true);
        // Then add the new vote
        const response = await apiService.voteAnswer(answerId, userId, voteType);
        if (!response.error) {
          console.log('Answer vote changed successfully');
        } else {
          // Revert optimistic update on error
          setAnswers(prev => prev.map(answer => 
            answer.id === answerId 
              ? { ...answer, votes: answer.votes - voteDelta }
              : answer
          ));
          console.error('Failed to change vote on answer:', response.error);
        }
      } else {
        // We're adding a new vote
        const response = await apiService.voteAnswer(answerId, userId, voteType);
        if (!response.error) {
          console.log('Answer vote recorded successfully');
        } else {
          // Revert optimistic update on error
          setAnswers(prev => prev.map(answer => 
            answer.id === answerId 
              ? { ...answer, votes: answer.votes - voteDelta }
              : answer
          ));
          console.error('Failed to vote on answer:', response.error);
        }
      }
    } catch (error) {
      // Revert optimistic update on error
      setAnswers(prev => prev.map(answer => 
        answer.id === answerId 
          ? { ...answer, votes: answer.votes - voteDelta }
          : answer
      ));
      console.error('Error voting on answer:', error);
    } finally {
      setVotingStates(prev => ({
        ...prev,
        answers: {
          ...prev.answers,
          [answerId]: { isVoting: false, userVote: newVote }
        }
      }));
    }
  };

  const handleAnswerSubmit = async (answerData: { question_id: number; user_id: number; body: string }) => {
    try {
      const response = await fetch('http://localhost:8000/answers/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(answerData)
      });

      if (response.ok) {
        const newAnswer = await response.json();
        console.log('Answer posted successfully:', newAnswer);
        
        // Refresh answers list
        const answersResponse = await fetch(`http://localhost:8000/answers/?question_id=${questionId}`);
        if (answersResponse.ok) {
          const updatedAnswers = await answersResponse.json();
          setAnswers(updatedAnswers);
          console.log('Updated answers list:', updatedAnswers);
        }
        
        return { success: true };
      } else {
        console.error('Failed to post answer:', response.status);
        return { success: false, error: 'Failed to post answer' };
      }
    } catch (error) {
      console.error('Error posting answer:', error);
      return { success: false, error: 'Network error' };
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading question...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-gray-600">Question not found</div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Question Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{question.title}</h1>
        
        <div className="flex items-center gap-4 text-sm text-gray-600 mb-6">
          <span>Asked {new Date(question.asked).toLocaleDateString()}</span>
          {question.modified && (
            <span>Modified {new Date(question.modified).toLocaleDateString()}</span>
          )}
          <span>Viewed {question.views} times</span>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-6">
          {question.tags.map((tag) => (
            <Link
              key={tag}
              href={`/questions/tagged/${tag}`}
              className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm hover:bg-blue-200"
            >
              {tag}
            </Link>
          ))}
        </div>
      </div>

      {/* Question Content */}
      <div className="flex gap-6 mb-8">
        {/* Vote Column */}
        <div className="flex flex-col items-center space-y-2">
          <button 
            className={`p-2 rounded border transition-colors ${
              votingStates.question?.userVote === 'up' 
                ? 'bg-orange-100 border-orange-300 text-orange-600' 
                : 'hover:bg-gray-100 border-gray-300 text-gray-600'
            } ${votingStates.question?.isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
            onClick={() => handleQuestionVote('up')}
            disabled={votingStates.question?.isVoting}
            title="This question shows research effort; it is useful and clear"
          >
            {votingStates.question?.isVoting && votingStates.question?.userVote === 'up' ? (
              <Loader2 className="w-8 h-8 animate-spin" />
            ) : (
              <ArrowUp className="w-8 h-8" />
            )}
          </button>
          <span className={`text-2xl font-semibold ${
            question.votes > 0 ? 'text-green-600' : 
            question.votes < 0 ? 'text-red-600' : 'text-gray-700'
          }`}>
            {question.votes}
          </span>
          <button 
            className={`p-2 rounded border transition-colors ${
              votingStates.question?.userVote === 'down' 
                ? 'bg-red-100 border-red-300 text-red-600' 
                : 'hover:bg-gray-100 border-gray-300 text-gray-600'
            } ${votingStates.question?.isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
            onClick={() => handleQuestionVote('down')}
            disabled={votingStates.question?.isVoting}
            title="This question does not show any research effort; it is unclear or not useful"
          >
            <ArrowDown className="w-8 h-8" />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded border border-gray-300 text-gray-600">
            <Bookmark className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="prose max-w-none mb-6" dangerouslySetInnerHTML={{ __html: question.content }} />
          
          {/* Author Info */}
          <div className="flex justify-end">
            <div className="bg-blue-50 p-4 rounded">
              <div className="text-xs text-gray-600 mb-2">asked {new Date(question.asked).toLocaleDateString()}</div>
              <div className="flex items-center space-x-3">
                <Image
                  src={question.author.avatar || `https://www.gravatar.com/avatar/${question.author.id}?s=32&d=identicon&r=PG`}
                  alt={question.author.name}
                  width={32}
                  height={32}
                  className="rounded"
                />
                <div>
                  <div className="font-semibold text-blue-600">{question.author.name}</div>
                  <div className="text-xs text-gray-600">{question.author.reputation}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Question Comments */}
      <CommentSection
        questionId={question.id}
        comments={questionComments}
        onCommentsUpdated={refreshQuestionComments}
      />

      {/* Answers Section */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">
            {answers.length} Answer{answers.length !== 1 ? 's' : ''}
          </h2>
        </div>

        {/* Real Answers from API */}
        {answers.map((answer) => (
          <div key={answer.id} className="mb-8 border-b border-gray-200 pb-8">
            <div className="flex space-x-6">
              {/* Vote Column */}
              <div className="flex flex-col items-center space-y-2">
                <button 
                  className={`p-2 rounded border transition-colors ${
                    votingStates.answers[answer.id]?.userVote === 'up' 
                      ? 'bg-orange-100 border-orange-300 text-orange-600' 
                      : 'hover:bg-gray-100 border-gray-300 text-gray-600'
                  } ${votingStates.answers[answer.id]?.isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
                  onClick={() => handleAnswerVote(answer.id, 'up')}
                  disabled={votingStates.answers[answer.id]?.isVoting}
                  title="This answer is useful"
                >
                  <ArrowUp className="w-6 h-6" />
                </button>
                <span className={`text-2xl font-semibold ${
                  answer.votes > 0 ? 'text-green-600' : 
                  answer.votes < 0 ? 'text-red-600' : 'text-gray-700'
                }`}>
                  {answer.votes}
                </span>
                <button 
                  className={`p-2 rounded border transition-colors ${
                    votingStates.answers[answer.id]?.userVote === 'down' 
                      ? 'bg-red-100 border-red-300 text-red-600' 
                      : 'hover:bg-gray-100 border-gray-300 text-gray-600'
                  } ${votingStates.answers[answer.id]?.isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
                  onClick={() => handleAnswerVote(answer.id, 'down')}
                  disabled={votingStates.answers[answer.id]?.isVoting}
                  title="This answer is not useful"
                >
                  <ArrowDown className="w-6 h-6" />
                </button>
                {answer.is_accepted && (
                  <CheckCircle className="w-6 h-6 text-green-600" />
                )}
              </div>

              {/* Answer Content */}
              <div className="flex-1">
                <div className="prose max-w-none mb-4">
                  <p>{answer.body}</p>
                </div>
                
                {/* Answer Author Info */}
                <div className="flex justify-end">
                  <div className="bg-blue-50 p-3 rounded">
                    <div className="text-xs text-gray-600 mb-2">
                      answered {new Date(answer.created_at).toLocaleDateString()}
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-6 h-6 bg-gray-300 rounded"></div>
                      <div>
                        <div className="font-semibold text-blue-600">User {answer.author_id}</div>
                        <div className="text-xs text-gray-600">Reputation: 100</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Answer Comments - Now positioned below the answer */}
            <CommentSection
              answerId={answer.id}
              comments={answerComments[answer.id] || []}
              onCommentsUpdated={() => refreshAnswerComments(answer.id)}
            />
          </div>
        ))}

        {/* Answer Form */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4">Your Answer</h3>
          <AnswerForm 
            questionId={questionId}
            onAnswerSubmitted={handleAnswerSubmit}
          />
        </div>
      </div>
    </div>
  );
}
