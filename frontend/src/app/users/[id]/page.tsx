"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import Link from "next/link";
import type { Question } from "@/lib/sampleData";
import { useAnalytics } from "@/hooks/useAnalytics";

interface TabProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const Tab = ({ label, isActive, onClick }: TabProps) => {
  const { handleClick } = useAnalytics();
  
  return (
    <button
      onClick={(e) => {
        onClick();
        handleClick('user-profile-tab', `User clicked on ${label} tab`, e);
      }}
      className={`px-4 py-2 ${
        isActive
          ? "border-b-2 border-orange-500 text-black"
          : "text-gray-600 hover:text-black"
      }`}
    >
      {label}
    </button>
  );
};

const QuestionCard = ({ question }: { question: Question }) => {
  const { handleClick } = useAnalytics();
  
  return (
    <div className="border-b border-gray-200 py-4 last:border-b-0">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <Link 
            href={`/questions/${question.id}`}
            className="text-lg font-medium text-blue-600 hover:text-blue-800 block mb-2"
            onClick={(e) => handleClick('user-question-link', `User clicked on question: "${question.title}" from profile`, e)}
          >
            {question.title}
          </Link>
          <p className="text-gray-600 text-sm line-clamp-2 mb-3">
            {question.content}
          </p>
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>{question.votes} votes</span>
            <span>{question.answers.length} answers</span>
            <span>{question.views} views</span>
            <span>asked {question.asked}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 ml-4">
          {question.tags.map((tag) => (
            <span
              key={tag}
              className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs whitespace-nowrap cursor-pointer hover:bg-blue-200"
              onClick={(e) => handleClick('user-profile-question-tag', `User clicked on tag "${tag}" from user profile question`, e)}
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default function UserProfile() {
  const { user } = useAuth();
  const params = useParams();
  const [activeTab, setActiveTab] = useState("Profile");
  const [userQuestions, setUserQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { handleClick } = useAnalytics();

  useEffect(() => {
    const fetchUserQuestions = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await fetch(`/api/users/${params.id}/questions?page=1&limit=10`);
        if (!response.ok) {
          throw new Error('Failed to fetch questions');
        }
        const data = await response.json();
        setUserQuestions(data.items); // The API returns items in a PaginatedResponse format
      } catch (err) {
        setError('Failed to load questions');
        console.error('Error fetching questions:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserQuestions();
  }, [params.id]);

  // Stats for the profile
  const stats = {
    reputation: 1,
    reached: userQuestions.reduce((acc, q) => acc + (typeof q.views === 'string' ? parseInt(q.views) : q.views), 0),
    answers: 0,
    questions: userQuestions.length,
  };

  const tabs = ["Profile", "Activity", "Saves", "Settings"];

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Profile Header */}
      <div className="flex items-start gap-6 mb-8">
        <div className="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center text-4xl font-bold text-white bg-blue-500">
          {user?.name?.charAt(0)?.toUpperCase() || "U"}
        </div>
        
        <div className="flex-1">
          <h1 className="text-3xl font-bold mb-2">{user?.name || "User"}</h1>
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
            <span>Member since today</span>
            <span>•</span>
            <span>Last seen this week</span>
            <span>•</span>
            <span>Visited 1 day, 1 consecutive</span>
          </div>
          
          <div className="flex gap-2">
            <Link 
              href="/users/edit"
              className="px-3 py-1.5 border border-gray-300 rounded-md hover:bg-gray-50"
              onClick={(e) => handleClick('edit-profile-button', 'User clicked Edit profile button', e)}
            >
              Edit profile
            </Link>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex gap-4">
          {tabs.map((tab) => (
            <Tab
              key={tab}
              label={tab}
              isActive={activeTab === tab}
              onClick={() => setActiveTab(tab)}
            />
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-4 gap-6">
        {/* Left Sidebar - Stats */}
        <div className="col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h2 className="text-xl font-bold mb-4">Stats</h2>
            <div className="space-y-4">
              <div>
                <div className="text-2xl font-bold">{stats.reputation}</div>
                <div className="text-sm text-gray-600">reputation</div>
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.reached}</div>
                <div className="text-sm text-gray-600">people reached</div>
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.answers}</div>
                <div className="text-sm text-gray-600">answers</div>
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.questions}</div>
                <div className="text-sm text-gray-600">questions</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="col-span-3">
          {activeTab === "Profile" && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-bold mb-4">About</h2>
                <p className="text-gray-600">
                  {user?.profile?.about?.bio || "Your about section appears empty. Tell the community about yourself!"}
                </p>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-bold mb-4">Links</h2>
                {user?.profile?.links?.website || user?.profile?.links?.twitter || user?.profile?.links?.github ? (
                  <div className="space-y-2">
                    {user?.profile?.links?.website && (
                      <a 
                        href={user.profile.links.website} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="block text-blue-600 hover:text-blue-800"
                        onClick={(e) => handleClick('user-profile-website-link', `User clicked website link: ${user.profile?.links?.website}`, e)}
                      >
                        🔗 {user.profile.links.website}
                      </a>
                    )}
                    {user?.profile?.links?.twitter && (
                      <a 
                        href={`https://twitter.com/${user.profile.links.twitter.replace('@', '')}`} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="block text-blue-600 hover:text-blue-800"
                        onClick={(e) => handleClick('user-profile-twitter-link', `User clicked Twitter link: ${user.profile?.links?.twitter}`, e)}
                      >
                        𝕏 {user.profile.links.twitter}
                      </a>
                    )}
                    {user?.profile?.links?.github && (
                      <a 
                        href={`https://github.com/${user.profile.links.github.replace('@', '')}`} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="block text-blue-600 hover:text-blue-800"
                        onClick={(e) => handleClick('user-profile-github-link', `User clicked GitHub link: ${user.profile?.links?.github}`, e)}
                      >
                        📧 {user.profile.links.github}
                      </a>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-500">No links to show</p>
                )}
              </div>

              {/* Questions Section */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-bold">Questions ({stats.questions})</h2>
                  {stats.questions > 0 && (
                    <Link 
                      href={`/users/${params.id}/questions`}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                      onClick={(e) => handleClick('view-all-questions-link', 'User clicked view all questions link', e)}
                    >
                      View all →
                    </Link>
                  )}
                </div>
                
                {isLoading ? (
                  <div className="text-center py-8">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
                    <p className="mt-2 text-gray-600">Loading questions...</p>
                  </div>
                ) : error ? (
                  <div className="text-center py-8">
                    <p className="text-red-600">{error}</p>
                  </div>
                ) : userQuestions.length > 0 ? (
                  <div className="space-y-4">
                    {userQuestions.slice(0, 5).map((question) => (
                      <QuestionCard key={question.id} question={question} />
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 py-8 text-center">No questions to show</p>
                )}
              </div>
            </div>
          )}

          {activeTab === "Activity" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-xl font-bold mb-4">Activity</h2>
              <p className="text-gray-500">No activity to show</p>
            </div>
          )}

          {activeTab === "Saves" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-xl font-bold mb-4">Saves</h2>
              <p className="text-gray-500">No saves to show</p>
            </div>
          )}

          {activeTab === "Settings" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-xl font-bold mb-4">Settings</h2>
              <Link 
                href="/users/edit"
                className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                onClick={(e) => handleClick('settings-edit-profile', 'User clicked Edit Profile from Settings', e)}
              >
                Edit Profile
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 