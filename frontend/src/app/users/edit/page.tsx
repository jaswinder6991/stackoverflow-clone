"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { useRouter } from "next/navigation";
import apiService from "@/services/api";

export default function EditProfile() {
  const { user, updateUser, refreshUser } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    displayName: user?.name || "",
    location: user?.profile?.basic?.location || "",
    title: user?.profile?.basic?.title || "",
    aboutMe: user?.profile?.about?.bio || "",
    links: {
      website: user?.profile?.links?.website || "",
      twitter: user?.profile?.links?.twitter || "",
      github: user?.profile?.links?.github || "",
    }
  });

  const handleInputChange = (field: string, value: string) => {
    if (field.startsWith("links.")) {
      const linkField = field.split(".")[1];
      setFormData(prev => ({
        ...prev,
        links: {
          ...prev.links,
          [linkField]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateUser({
        basic: {
          displayName: formData.displayName,
          location: formData.location,
          title: formData.title,
        },
        about: {
          bio: formData.aboutMe,
        },
        links: formData.links,
      });
      // Refresh user data before redirecting
      await refreshUser();
      router.push(`/users/${user?.id}`);
    } catch (error) {
      console.error("Failed to update profile:", error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-6">Edit your profile</h1>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Public Information */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Public information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Display name
              </label>
              <input
                type="text"
                value={formData.displayName}
                onChange={(e) => handleInputChange("displayName", e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location
              </label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => handleInputChange("location", e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange("title", e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="No title has been set"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                About me
              </label>
              <div className="border border-gray-300 rounded-md">
                <div className="border-b border-gray-300 px-2 py-1 bg-gray-50">
                  <div className="flex gap-2">
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span className="font-bold">B</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded italic">
                      <span>I</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>🔗</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>"</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>{`{}`}</span>
                    </button>
                    <div className="h-4 w-px bg-gray-300 mx-1"></div>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>•</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>1.</span>
                    </button>
                    <button type="button" className="p-1 hover:bg-gray-200 rounded">
                      <span>=</span>
                    </button>
                  </div>
                </div>
                <textarea
                  value={formData.aboutMe}
                  onChange={(e) => handleInputChange("aboutMe", e.target.value)}
                  rows={8}
                  className="w-full px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Links */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Links</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Website link
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500">🔗</span>
                </div>
                <input
                  type="url"
                  value={formData.links.website}
                  onChange={(e) => handleInputChange("links.website", e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="https://example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                X link or username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500">𝕏</span>
                </div>
                <input
                  type="text"
                  value={formData.links.twitter}
                  onChange={(e) => handleInputChange("links.twitter", e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="@username"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                GitHub link or username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.605-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12" />
                    </svg>
                  </span>
                </div>
                <input
                  type="text"
                  value={formData.links.github}
                  onChange={(e) => handleInputChange("links.github", e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="username"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Save profile
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
} 