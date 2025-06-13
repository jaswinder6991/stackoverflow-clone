import React from 'react';
import { ArrowUp, ArrowDown, Bookmark, Clock, CheckCircle } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

interface QuestionDetailProps {
  question: {
    id: number;
    title: string;
    content: string;
    author: {
      name: string;
      reputation: number;
      avatar: string;
      badges: {
        gold: number;
        silver: number;
        bronze: number;
      };
    };
    votes: number;
    views: string | number;
    asked: string;
    modified: string;
    tags: string[];
    answers: Answer[];
  };
}

interface Answer {
  id: number;
  content: string;
  author: {
    name: string;
    reputation: number;
    avatar: string;
    badges: {
      gold: number;
      silver: number;
      bronze: number;
    };
  };
  votes: number;
  isAccepted: boolean;
  answered: string;
}

export default function QuestionDetail({ question }: QuestionDetailProps) {
  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Question Header */}
      <div className="mb-6">
        <div className="flex justify-between items-start mb-4">
          <h1 className="text-2xl font-semibold text-gray-900 flex-1 mr-4">
            {question.title}
          </h1>
          <Link href="/ask" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
            Ask Question
          </Link>
        </div>
        
        <div className="flex items-center space-x-4 text-sm text-gray-600 border-b border-gray-200 pb-4">
          <div>
            <span className="text-gray-500">Asked</span> {question.asked}
          </div>
          <div>
            <span className="text-gray-500">Modified</span> {question.modified}
          </div>
          <div>
            <span className="text-gray-500">Viewed</span> {question.views} times
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="flex space-x-6 mb-8">
        {/* Vote Column */}
        <div className="flex flex-col items-center space-y-2">
          <button className="p-2 hover:bg-gray-100 rounded">
            <ArrowUp className="w-6 h-6 text-gray-600" />
          </button>
          <span className="text-2xl font-semibold text-gray-700">{question.votes}</span>
          <button className="p-2 hover:bg-gray-100 rounded">
            <ArrowDown className="w-6 h-6 text-gray-600" />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded">
            <Bookmark className="w-5 h-5 text-gray-600" />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded">
            <Clock className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Question Body */}
        <div className="flex-1">
          <div className="prose max-w-none mb-6">
            <p className="text-gray-800 leading-relaxed">{question.content}</p>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-6">
            {question.tags.map((tag) => (
              <span
                key={tag}
                className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm hover:bg-blue-200 cursor-pointer"
              >
                {tag}
              </span>
            ))}
          </div>

          {/* Actions and Author */}
          <div className="flex justify-between items-end">
            <div className="flex space-x-4 text-sm text-gray-600">
              <button className="hover:text-blue-600">Share</button>
              <button className="hover:text-blue-600">Edit</button>
              <button className="hover:text-blue-600">Follow</button>
              <button className="hover:text-blue-600">Flag</button>
            </div>
            
            <div className="bg-blue-50 p-3 rounded">
              <div className="text-xs text-gray-600 mb-2">
                edited {question.modified}
              </div>
              <div className="flex items-center space-x-2">
                <Image
                  src={question.author.avatar}
                  alt={question.author.name}
                  width={32}
                  height={32}
                  className="rounded"
                />
                <div>
                  <div className="font-medium text-blue-600">{question.author.name}</div>
                  <div className="text-xs text-gray-600">
                    {question.author.reputation.toLocaleString()}
                    <span className="ml-2">
                      <span className="text-yellow-600">●</span> {question.author.badges.gold}
                      <span className="ml-1 text-gray-500">●</span> {question.author.badges.silver}
                      <span className="ml-1 text-orange-600">●</span> {question.author.badges.bronze}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Answers Section */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">
            {question.answers.length} Answer{question.answers.length !== 1 ? 's' : ''}
          </h2>
          <div className="flex items-center space-x-4">
            <label className="text-sm text-gray-600">Sorted by:</label>
            <select className="border border-gray-300 rounded px-2 py-1 text-sm">
              <option>Highest score (default)</option>
              <option>Trending (recent votes count more)</option>
              <option>Date modified (newest first)</option>
              <option>Date created (oldest first)</option>
            </select>
          </div>
        </div>

        {/* Answers */}
        {question.answers.map((answer) => (
          <div key={answer.id} className="flex space-x-6 mb-8 border-b border-gray-200 pb-8">
            {/* Vote Column */}
            <div className="flex flex-col items-center space-y-2">
              <button className="p-2 hover:bg-gray-100 rounded">
                <ArrowUp className="w-6 h-6 text-gray-600" />
              </button>
              <span className="text-2xl font-semibold text-gray-700">{answer.votes}</span>
              <button className="p-2 hover:bg-gray-100 rounded">
                <ArrowDown className="w-6 h-6 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded">
                <Bookmark className="w-5 h-5 text-gray-600" />
              </button>
              {answer.isAccepted && (
                <div className="p-2 text-green-600">
                  <CheckCircle className="w-8 h-8" />
                </div>
              )}
              <button className="p-2 hover:bg-gray-100 rounded">
                <Clock className="w-5 h-5 text-gray-600" />
              </button>
            </div>

            {/* Answer Body */}
            <div className="flex-1">
              <div className="prose max-w-none mb-6">
                <div 
                  className="text-gray-800 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: answer.content }}
                />
              </div>

              {/* Actions and Author */}
              <div className="flex justify-between items-end">
                <div className="flex space-x-4 text-sm text-gray-600">
                  <button className="hover:text-blue-600">Share</button>
                  <button className="hover:text-blue-600">Edit</button>
                  <button className="hover:text-blue-600">Follow</button>
                  <button className="hover:text-blue-600">Flag</button>
                </div>
                
                <div className="bg-blue-50 p-3 rounded">
                  <div className="text-xs text-gray-600 mb-2">
                    answered {answer.answered}
                  </div>
                  <div className="flex items-center space-x-2">
                    <Image
                      src={answer.author.avatar}
                      alt={answer.author.name}
                      width={32}
                      height={32}
                      className="rounded"
                    />
                    <div>
                      <div className="font-medium text-blue-600">{answer.author.name}</div>
                      <div className="text-xs text-gray-600">
                        {answer.author.reputation.toLocaleString()}
                        <span className="ml-2">
                          <span className="text-yellow-600">●</span> {answer.author.badges.gold}
                          <span className="ml-1 text-gray-500">●</span> {answer.author.badges.silver}
                          <span className="ml-1 text-orange-600">●</span> {answer.author.badges.bronze}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
