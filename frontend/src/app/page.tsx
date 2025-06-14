'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Layout from '@/components/Layout';
import TopNav from '@/components/TopNav';
import apiService from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';

export default function HomePage() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchQuestions = async () => {
      setLoading(true);
      setError(null);
      try {
        const res: any = await apiService.getQuestions();
        // Defensive: handle undefined or unexpected response
        const items = res?.data?.items && Array.isArray(res.data.items) ? res.data.items : [];
        setQuestions(items);
      } catch (err: any) {
        setError('Failed to load questions.');
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, []);

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Content */}
        <div className="flex">
          <div className="flex-1">
            {/* Login prompt */}
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-3xl font-bold">Top Questions</h1>
              <Link href="/questions/ask">
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Ask Question
                </button>
              </Link>
            </div>
            {loading && (
              <div className="text-center py-8 text-gray-500">Loading questions…</div>
            )}
            {error && (
              <div className="text-center py-8 text-red-500">{error}</div>
            )}
            {!loading && !error && questions.length === 0 && (
              <div className="text-center py-8 text-gray-500">No questions found.</div>
            )}
            {!loading && !error && questions.map((question: any) => (
              <div key={question.id} className="bg-white border border-gray-300 rounded p-4 mb-4">
                <div className="flex justify-between items-start mb-3">
                  <Link href={`/questions/${question.id}`}>
                    <h2 className="text-lg font-medium text-blue-600 hover:text-blue-800 cursor-pointer">
                      {question.title}
                    </h2>
                  </Link>
                  <div className="flex space-x-4 text-sm text-gray-600">
                    <span>{question.votes} votes</span>
                    <span>{question.answer_count ?? 0} answers</span>
                    <span>{question.views} views</span>
                  </div>
                </div>
                <p className="text-gray-700 mb-3">{question.content}</p>
                <div className="flex items-center justify-between">
                  <div className="flex space-x-2">
                    {question.tags && question.tags.map((tag: string) => (
                      <span
                        key={tag}
                        className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="text-sm text-gray-600">
                    asked {question.asked} by <span className="text-blue-600">{question.author?.name}</span>
                  </div>
                </div>
              </div>
            ))}
            {/* Pagination */}
            <div className="flex justify-center mt-8">
              <div className="flex space-x-2">
                <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">Prev</button>
                <button className="px-3 py-2 bg-orange-500 text-white rounded">1</button>
                <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">2</button>
                <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">3</button>
                <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">Next</button>
              </div>
            </div>
          </div>
          {/* Right Sidebar */}
        </div>
      </div>
    </Layout>
  );
}
