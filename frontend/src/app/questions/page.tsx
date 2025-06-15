'use client';

import { generateSampleQuestion } from '@/lib/sampleData';
import Layout from '@/components/Layout';
import { useAnalytics } from '@/hooks/useAnalytics';
import { useRouter } from 'next/navigation';

export default function QuestionsPage() {
  const { handleClick } = useAnalytics();
  const router = useRouter();
  
  // Generate sample questions
  const questions = Array.from({ length: 10 }, (_, i) => generateSampleQuestion(i + 1));

    return (
    <Layout>
      <div className="p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">All Questions</h1>
            <button 
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              onClick={(e) => {
                handleClick('ask-question-button', 'User clicked Ask Question button from questions page', e);
                router.push('/ask');
              }}
            >
              Ask Question
            </button>
          </div>
          
          {questions.map((question) => (
            <div key={question.id} className="bg-white border border-gray-300 rounded p-4 mb-4">
              <div className="flex justify-between items-start mb-3">
                <h2 
                  className="text-lg font-medium text-blue-600 hover:text-blue-800 cursor-pointer"
                  onClick={(e) => {
                    handleClick('question-title', `User clicked on question: "${question.title}"`, e);
                    router.push(`/questions/${question.id}`);
                  }}
                >
                  {question.title}
                </h2>
                <div className="flex space-x-4 text-sm text-gray-600">
                  <span>{question.votes} votes</span>
                  <span>{question.answers.length} answers</span>
                  <span>{question.views} views</span>
                </div>
              </div>
              <p className="text-gray-700 mb-3">
                {question.content}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex space-x-2">
                  {question.tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs cursor-pointer hover:bg-blue-200"
                      onClick={(e) => {
                        handleClick('question-tag', `User clicked on tag: "${tag}"`, e);
                        router.push(`/questions/tagged/${tag}`);
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="text-sm text-gray-600">
                  asked {question.asked} by 
                  <span 
                    className="text-blue-600 cursor-pointer hover:underline ml-1"
                    onClick={(e) => {
                      handleClick('question-author', `User clicked on author: "${question.author.name}"`, e);
                      router.push(`/users/${question.author.id}`);
                    }}
                  >
                    {question.author.name}
                  </span>
                </div>
              </div>
            </div>
          ))}

          {/* Pagination */}
          <div className="flex justify-center mt-8">
            <div className="flex space-x-2">
              <button 
                className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50"
                onClick={(e) => handleClick('pagination-prev', 'User clicked Previous page', e)}
              >
                Prev
              </button>
              <button 
                className="px-3 py-2 bg-orange-500 text-white rounded"
                onClick={(e) => handleClick('pagination-page', 'User clicked page 1', e)}
              >
                1
              </button>
              <button 
                className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50"
                onClick={(e) => handleClick('pagination-page', 'User clicked page 2', e)}
              >
                2
              </button>
              <button 
                className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50"
                onClick={(e) => handleClick('pagination-page', 'User clicked page 3', e)}
              >
                3
              </button>
              <button 
                className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50"
                onClick={(e) => handleClick('pagination-next', 'User clicked Next page', e)}
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
