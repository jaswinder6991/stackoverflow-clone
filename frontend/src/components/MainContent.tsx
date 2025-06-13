"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { generateSampleQuestions, Question } from '@/lib/sampleData';

const MainContent = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [mounted, setMounted] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    setMounted(true);
    setQuestions(generateSampleQuestions(15));
  }, []);

  if (!mounted) {
    return (
      <div className="flex-1 min-w-0">
        <div className="animate-pulse">
          {/* Loading state */}
          <div className="mb-8">
            <div className="h-8 bg-gray-200 rounded w-80 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-96"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-w-0">
      {/* Welcome Section */}
      <div className="mb-8">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
              Welcome back, {user?.username}
            </h1>
            <p className="text-gray-600">
              Find answers to your technical questions and help others answer theirs.
            </p>
          </div>
          <Link 
            href="/questions/ask" 
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded hover:bg-blue-700 transition-colors whitespace-nowrap"
          >
            Ask Question
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Reputation Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium">Reputation</h3>
            <span className="text-2xl font-bold text-gray-900">+70</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Current</span>
              <span className="font-medium">2,584</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Next privilege</span>
              <span className="font-medium">3,000</span>
            </div>
            <div className="mt-2 h-2 bg-gray-100 rounded-full">
              <div className="h-2 bg-green-500 rounded-full" style={{ width: '86%' }}></div>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              416 reputation until Cast close & reopen votes
            </p>
          </div>
        </div>

        {/* Badges Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium">Badges</h3>
            <div className="flex items-center space-x-2">
              <span className="text-yellow-500">●</span>
              <span className="font-bold">2</span>
              <span className="text-gray-400">●</span>
              <span className="font-bold">23</span>
              <span className="text-orange-500">●</span>
              <span className="font-bold">25</span>
            </div>
          </div>
          <div className="space-y-3">
            <div>
              <div className="text-sm font-medium mb-1">Next badge:</div>
              <div className="text-sm text-gray-600">Excavator</div>
              <div className="text-xs text-gray-500">
                Edit first post that was inactive for 6 months
              </div>
            </div>
            <div className="h-2 bg-gray-100 rounded-full">
              <div className="h-2 bg-blue-500 rounded-full" style={{ width: '0%' }}></div>
            </div>
            <div className="text-xs text-gray-500">0 / 1 progress</div>
          </div>
        </div>

        {/* Tags Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium">Your Tags</h3>
            <Link href="/users/edit/tags" className="text-sm text-blue-600 hover:text-blue-800">
              Edit watched tags
            </Link>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm">angular</span>
            <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm">nodejs-server</span>
            <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm">postgresql</span>
            <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm">spring</span>
            <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-sm">typescript</span>
          </div>
        </div>
      </div>

      {/* Interesting Posts */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-medium">Interesting posts for you</h2>
          <p className="text-sm text-gray-600">Based on your viewing history and watched tags</p>
        </div>
        <div className="divide-y divide-gray-200">
          {questions.slice(0, 5).map((question) => (
            <div key={question.id} className="p-4 hover:bg-gray-50">
              <div className="flex justify-between items-start mb-2">
                <Link 
                  href={`/questions/${question.id}`}
                  className="text-lg font-medium text-blue-600 hover:text-blue-800"
                >
                  {question.title}
                </Link>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <span>{question.votes} votes</span>
                  <span>{question.answers.length} answers</span>
                  <span>{question.views} views</span>
                </div>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {question.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-xs"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainContent;
