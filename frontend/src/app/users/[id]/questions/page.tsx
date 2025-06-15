"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useParams, useSearchParams } from "next/navigation";
import { useState, useEffect } from "react";
import Link from "next/link";
import type { Question } from "@/lib/sampleData";
import { useAnalytics } from "@/hooks/useAnalytics";
import apiService from "@/services/api";

interface SortOption {
  value: string;
  label: string;
}

const sortOptions: SortOption[] = [
  { value: "newest", label: "Newest" },
  { value: "votes", label: "Most Votes" },
  { value: "active", label: "Most Active" },
];

const QuestionCard = ({ question }: { question: Question }) => {
  const { handleClick } = useAnalytics();
  
  return (
    <div className="border border-gray-200 rounded-lg p-6 bg-white hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <Link 
            href={`/questions/${question.id}`}
            className="text-xl font-medium text-blue-600 hover:text-blue-800 block mb-3"
            onClick={(e) => handleClick('user-questions-page-link', `User clicked on question: "${question.title}"`, e)}
          >
            {question.title}
          </Link>
          <p className="text-gray-600 text-sm line-clamp-3 mb-4">
            {question.content}
          </p>
          <div className="flex items-center space-x-6 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <span className="font-medium">{question.votes}</span>
              <span>votes</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="font-medium">{question.answers?.length || 0}</span>
              <span>answers</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="font-medium">{question.views}</span>
              <span>views</span>
            </span>
            <span>asked {question.asked}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 ml-6">
          {question.tags.map((tag) => (
            <span
              key={tag}
              className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs whitespace-nowrap cursor-pointer hover:bg-blue-200"
              onClick={(e) => handleClick('user-questions-tag', `User clicked on tag "${tag}" from user questions page`, e)}
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

const Pagination = ({ 
  currentPage, 
  totalPages, 
  onPageChange 
}: { 
  currentPage: number; 
  totalPages: number; 
  onPageChange: (page: number) => void; 
}) => {
  const { handleClick } = useAnalytics();
  
  if (totalPages <= 1) return null;

  const pages = [];
  const maxVisible = 5;
  
  let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
  let endPage = Math.min(totalPages, startPage + maxVisible - 1);
  
  if (endPage - startPage + 1 < maxVisible) {
    startPage = Math.max(1, endPage - maxVisible + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <div className="flex items-center justify-center space-x-2 mt-8">
      {currentPage > 1 && (
        <button
          onClick={(e) => {
            onPageChange(currentPage - 1);
            handleClick('pagination-prev', 'User clicked previous page', e);
          }}
          className="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Previous
        </button>
      )}
      
      {startPage > 1 && (
        <>
          <button
            onClick={(e) => {
              onPageChange(1);
              handleClick('pagination-first', 'User clicked first page', e);
            }}
            className="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            1
          </button>
          {startPage > 2 && <span className="px-2">...</span>}
        </>
      )}
      
      {pages.map((page) => (
        <button
          key={page}
          onClick={(e) => {
            onPageChange(page);
            handleClick('pagination-page', `User clicked page ${page}`, e);
          }}
          className={`px-3 py-2 text-sm rounded-md ${
            page === currentPage
              ? "bg-orange-500 text-white"
              : "bg-white border border-gray-300 hover:bg-gray-50"
          }`}
        >
          {page}
        </button>
      ))}
      
      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && <span className="px-2">...</span>}
          <button
            onClick={(e) => {
              onPageChange(totalPages);
              handleClick('pagination-last', 'User clicked last page', e);
            }}
            className="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {totalPages}
          </button>
        </>
      )}
      
      {currentPage < totalPages && (
        <button
          onClick={(e) => {
            onPageChange(currentPage + 1);
            handleClick('pagination-next', 'User clicked next page', e);
          }}
          className="px-3 py-2 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Next
        </button>
      )}
    </div>
  );
};

export default function UserQuestionsPage() {
  const { user } = useAuth();
  const params = useParams();
  const searchParams = useSearchParams();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [currentSort, setCurrentSort] = useState("newest");
  const [userData, setUserData] = useState<any>(null);
  const { handleClick } = useAnalytics();

  const questionsPerPage = 15;

  useEffect(() => {
    const page = parseInt(searchParams.get('page') || '1');
    const sort = searchParams.get('sort') || 'newest';
    setCurrentPage(page);
    setCurrentSort(sort);
  }, [searchParams]);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await apiService.getUser(parseInt(params.id as string));
        if (response.error) {
          throw new Error(response.error);
        }
        setUserData(response.data);
      } catch (err) {
        console.error('Error fetching user data:', err);
      }
    };

    fetchUserData();
  }, [params.id]);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await apiService.getQuestionsByUser(
          parseInt(params.id as string),
          {
            skip: (currentPage - 1) * questionsPerPage,
            limit: questionsPerPage,
            sort: currentSort
          }
        );
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        const data = response.data as any;
        setQuestions(data?.items || []);
        setTotalQuestions(data?.total || 0);
        setTotalPages(Math.ceil((data?.total || 0) / questionsPerPage));
        
      } catch (err) {
        setError('Failed to load questions');
        console.error('Error fetching questions:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuestions();
  }, [params.id, currentPage, currentSort]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    const url = new URL(window.location.href);
    url.searchParams.set('page', page.toString());
    url.searchParams.set('sort', currentSort);
    window.history.pushState({}, '', url.toString());
  };

  const handleSortChange = (sort: string) => {
    setCurrentSort(sort);
    setCurrentPage(1);
    const url = new URL(window.location.href);
    url.searchParams.set('page', '1');
    url.searchParams.set('sort', sort);
    window.history.pushState({}, '', url.toString());
  };

  if (isLoading && !questions.length) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
          <p className="mt-4 text-gray-600">Loading questions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <nav className="text-sm text-gray-600 mb-2">
            <Link href="/users" className="hover:text-blue-600">Users</Link>
            <span className="mx-2">›</span>
            <Link 
              href={`/users/${params.id}`} 
              className="hover:text-blue-600"
              onClick={(e) => handleClick('user-profile-breadcrumb', 'User clicked user profile breadcrumb', e)}
            >
              {userData?.name || 'User'}
            </Link>
            <span className="mx-2">›</span>
            <span>Questions</span>
          </nav>
          <h1 className="text-3xl font-bold">
            Questions by {userData?.name || 'User'} ({totalQuestions})
          </h1>
        </div>
        
        <Link 
          href={`/users/${params.id}`}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          onClick={(e) => handleClick('back-to-profile', 'User clicked back to profile button', e)}
        >
          Back to Profile
        </Link>
      </div>

      {/* Sort Options */}
      <div className="flex items-center gap-4 mb-6">
        <span className="text-sm text-gray-600">Sort by:</span>
        {sortOptions.map((option) => (
          <button
            key={option.value}
            onClick={(e) => {
              handleSortChange(option.value);
              handleClick('sort-questions', `User sorted questions by ${option.label}`, e);
            }}
            className={`px-3 py-1 text-sm rounded-md ${
              currentSort === option.value
                ? "bg-orange-500 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>

      {/* Questions List */}
      {error ? (
        <div className="text-center py-12">
          <p className="text-red-600 text-lg">{error}</p>
        </div>
      ) : questions.length > 0 ? (
        <div className="space-y-4">
          {questions.map((question) => (
            <QuestionCard key={question.id} question={question} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No questions found</p>
          <p className="text-gray-400 mt-2">This user hasn't asked any questions yet.</p>
        </div>
      )}

      {/* Pagination */}
      <Pagination 
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
      />
    </div>
  );
} 