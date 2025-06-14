"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useParams } from "next/navigation";
import { useState } from "react";
import Link from "next/link";

interface TabProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const Tab = ({ label, isActive, onClick }: TabProps) => (
  <button
    onClick={onClick}
    className={`px-4 py-2 ${
      isActive
        ? "border-b-2 border-orange-500 text-black"
        : "text-gray-600 hover:text-black"
    }`}
  >
    {label}
  </button>
);

export default function UserProfile() {
  const { user } = useAuth();
  const params = useParams();
  const [activeTab, setActiveTab] = useState("Profile");

  // Stats for the profile
  const stats = {
    reputation: 1,
    reached: 0,
    answers: 0,
    questions: 0,
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
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 ${
                activeTab === tab
                  ? "border-b-2 border-orange-500 text-black"
                  : "text-gray-600 hover:text-black"
              }`}
            >
              {tab}
            </button>
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
                      <a href={user.profile.links.website} target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">
                        🔗 {user.profile.links.website}
                      </a>
                    )}
                    {user?.profile?.links?.twitter && (
                      <a href={`https://twitter.com/${user.profile.links.twitter.replace('@', '')}`} target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">
                        𝕏 {user.profile.links.twitter}
                      </a>
                    )}
                    {user?.profile?.links?.github && (
                      <a href={`https://github.com/${user.profile.links.github}`} target="_blank" rel="noopener noreferrer" className="block text-blue-600 hover:text-blue-800">
                        <span className="inline-block align-text-bottom mr-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.605-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12" />
                          </svg>
                        </span>
                        {user.profile.links.github}
                      </a>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-600">No links have been added to your profile yet.</p>
                )}
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-bold mb-4">Posts</h2>
                <p className="text-gray-600">
                  You haven't created any posts yet. Start contributing to the community!
                </p>
              </div>
            </div>
          )}

          {activeTab === "Activity" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <p className="text-gray-600">No recent activity to show.</p>
            </div>
          )}

          {activeTab === "Saves" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <p className="text-gray-600">No saved items yet.</p>
            </div>
          )}

          {activeTab === "Settings" && (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-xl font-bold mb-4">Profile Settings</h2>
              <p className="text-gray-600">Profile settings coming soon.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 