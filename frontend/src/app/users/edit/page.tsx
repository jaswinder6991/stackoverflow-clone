"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { useRouter } from "next/navigation";
import apiService from "@/services/api";
import { useAnalytics } from "@/hooks/useAnalytics";

export default function EditProfile() {
  const { user, updateUser, refreshUser } = useAuth();
  const router = useRouter();
  const { handleClick, handleKeyPress } = useAnalytics();
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
    
    // Log the input change
    handleKeyPress(`edit-profile-${field}`, `User updated ${field} field`, value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    handleClick('save-profile-changes', 'User clicked Save Profile Changes button');
    
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
      handleClick('profile-update-success', 'User successfully updated profile');
      router.push(`/users/${user?.id}`);
    } catch (error) {
      console.error("Failed to update profile:", error);
      handleClick('profile-update-error', 'Profile update failed');
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
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-bold-button', 'User clicked Bold button in editor', e)}
                    >
                      <span className="font-bold">B</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded italic"
                      onClick={(e) => handleClick('editor-italic-button', 'User clicked Italic button in editor', e)}
                    >
                      <span>I</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-link-button', 'User clicked Link button in editor', e)}
                    >
                      <span>🔗</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-quote-button', 'User clicked Quote button in editor', e)}
                    >
                      <span>"</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-code-button', 'User clicked Code button in editor', e)}
                    >
                      <span>{`{}`}</span>
                    </button>
                    <div className="h-4 w-px bg-gray-300 mx-1"></div>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-bullet-button', 'User clicked Bullet list button in editor', e)}
                    >
                      <span>•</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-number-button', 'User clicked Number list button in editor', e)}
                    >
                      <span>1.</span>
                    </button>
                    <button 
                      type="button" 
                      className="p-1 hover:bg-gray-200 rounded"
                      onClick={(e) => handleClick('editor-heading-button', 'User clicked Heading button in editor', e)}
                    >
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
                  <span className="text-gray-500">📧</span>
                </div>
                <input
                  type="text"
                  value={formData.links.github}
                  onChange={(e) => handleInputChange("links.github", e.target.value)}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="@username"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between">
          <button
            type="button"
            onClick={(e) => {
              handleClick('cancel-edit-profile', 'User clicked Cancel button in edit profile', e);
              router.back();
            }}
            className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Save Profile
          </button>
        </div>
      </form>
    </div>
  );
} 