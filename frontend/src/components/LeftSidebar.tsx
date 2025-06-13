"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const LeftSidebar = () => {
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const isCurrentPath = (path: string) => {
    if (!mounted) return false;
    return pathname === path;
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex-shrink-0 sticky top-12 h-screen overflow-y-auto">
      <div className="p-4">
        <nav aria-label="Primary">
          <ul className="space-y-1">
            {/* Home */}
            <li>
              <Link href="/" className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                isCurrentPath('/') 
                  ? 'text-blue-600 bg-blue-50 border-r-2 border-blue-600' 
                  : 'text-gray-700 hover:bg-gray-100'
              }`}>
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M15 10v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5H0l9-9 9 9zm-8 1v6h4v-6z"/>
                </svg>
                Home
              </Link>
            </li>

            {/* Questions */}
            <li>
              <Link href="/questions" className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                isCurrentPath('/questions') 
                  ? 'text-blue-600 bg-blue-50 border-r-2 border-blue-600' 
                  : 'text-gray-700 hover:bg-gray-100'
              }`}>
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="m4 15-3 3V4c0-1.1.9-2 2-2h12c1.09 0 2 .91 2 2v9c0 1.09-.91 2-2 2zm7.75-3.97c.72-.83.98-1.86.98-2.94 0-1.65-.7-3.22-2.3-3.83a4.4 4.4 0 0 0-3.02 0 3.8 3.8 0 0 0-2.32 3.83q0 1.93 1.03 3a3.8 3.8 0 0 0 2.85 1.07q.94 0 1.71-.34.97.66 1.06.7.34.2.7.3l.59-1.13a5 5 0 0 1-1.28-.66m-1.27-.9a5 5 0 0 0-1.5-.8l-.45.9q.5.18.98.5-.3.1-.65.11-.92 0-1.52-.68c-.86-1-.86-3.12 0-4.11.8-.9 2.35-.9 3.15 0 .9 1.01.86 3.03-.01 4.08"/>
                </svg>
                Questions
              </Link>
            </li>

            {/* Staging Ground */}
            <li>
              <Link href="/staging-ground" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="m1 6 8-5 8 5v8h-2V7.09L9 11zm8 10.82L3 13V9l6 3.82 5-3.32v4z"/>
                </svg>
                Staging Ground
              </Link>
            </li>

            {/* Tags */}
            <li>
              <Link href="/tags" className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                isCurrentPath('/tags') 
                  ? 'text-blue-600 bg-blue-50 border-r-2 border-blue-600' 
                  : 'text-gray-700 hover:bg-gray-100'
              }`}>
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M9.24 1a3 3 0 0 0-2.12.88l-5.7 5.7a2 2 0 0 0-.38 2.31 3 3 0 0 1 .67-1.01l6-6A3 3 0 0 1 9.83 2H14a3 3 0 0 1 .79.1A2 2 0 0 0 13 1z" opacity=".4"/>
                  <path d="M9.83 3a2 2 0 0 0-1.42.59l-6 6a2 2 0 0 0 0 2.82L6.6 16.6a2 2 0 0 0 2.82 0l6-6A2 2 0 0 0 16 9.17V5a2 2 0 0 0-2-2zM12 9a2 2 0 1 1 0-4 2 2 0 0 1 0 4"/>
                </svg>
                Tags
              </Link>
            </li>

            {/* Saves */}
            <li>
              <Link href="/saves" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M3 17V3c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2v14l-6-4z"/>
                </svg>
                Saves
              </Link>
            </li>

            {/* Spacer */}
            <li className="pb-6"></li>

            {/* Challenges */}
            <li>
              <Link href="/challenges" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <div className="w-6 h-6 mr-2 bg-purple-500 rounded-full flex items-center justify-center">
                  <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 18 18">
                    <path d="M10.5 3.5 8 7.25l2 2.25L8.5 11l-3-3.5L1 14h16z"/>
                  </svg>
                </div>
                <span>Challenges</span>
                <span className="ml-auto px-1.5 py-0.5 text-xs bg-blue-100 text-blue-600 rounded">New</span>
              </Link>
            </li>

            {/* Chat */}
            <li>
              <Link href="/chat" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <div className="w-6 h-6 mr-2 bg-purple-500 rounded-full flex items-center justify-center">
                  <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 18 16">
                    <path d="M17 3C17 1.89543 16.1046 1 15 1H7C5.89543 1 5 1.89543 5 3V5C5 6.10457 5.89543 7 7 7H15C16.1046 7 17 6.10457 17 5V3ZM7 3H15V5H7V3Z"/>
                    <path d="M17 10C17 8.89543 16.1046 8 15 8H7C5.89543 8 5 8.89543 5 10V14C5 15.1046 5.89543 16 7 16H15C16.1046 16 17 15.1046 17 14V10ZM7 10H15V14H7V10Z"/>
                    <path d="M1 9C1 8.44771 1.44772 8 2 8H3C3.55228 8 4 8.44772 4 9V10C4 10.5523 3.55228 11 3 11H2C1.44772 11 1 10.5523 1 10V9Z"/>
                    <path d="M2 1C1.44772 1 1 1.44772 1 2V3C1 3.55228 1.44772 4 2 4H3C3.55228 4 4 3.55228 4 3V2C4 1.44772 3.55228 1 3 1H2Z"/>
                  </svg>
                </div>
                Chat
              </Link>
            </li>

            {/* Articles */}
            <li>
              <Link href="/articles" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M5 3a2 2 0 0 0-2 2v10c0 1.1.9 2 2 2h7a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm2 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0m-2 4.5c0-.28.22-.5.5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5m.5 1.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1 0-1M5 14.5c0-.28.22-.5.5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
                  <path d="M5.9 2h6.35A2.75 2.75 0 0 1 15 4.75v9.35c.62-.6 1-1.43 1-2.35v-7.5C16 2.45 14.54 1 12.75 1h-4.5c-.92 0-1.75.38-2.35 1" opacity=".4"/>
                </svg>
                Articles
              </Link>
            </li>

            {/* Users */}
            <li>
              <Link href="/users" className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                isCurrentPath('/users') 
                  ? 'text-blue-600 bg-blue-50 border-r-2 border-blue-600' 
                  : 'text-gray-700 hover:bg-gray-100'
              }`}>
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M17 14c0 .44-.45 1-1 1H9a1 1 0 0 1-1-1H2c-.54 0-1-.56-1-1 0-2.63 3-4 3-4s.23-.4 0-1c-.84-.62-1.06-.59-1-3s1.37-3 2.5-3 2.44.58 2.5 3-.16 2.38-1 3c-.23.59 0 1 0 1s1.55.71 2.42 2.09c.78-.72 1.58-1.1 1.58-1.1s.23-.4 0-1c-.84-.61-1.06-.58-1-3s1.37-3 2.5-3 2.44.59 2.5 3c.05 2.42-.16 2.39-1 3-.23.6 0 1 0 1s3 1.38 3 4"/>
                </svg>
                Users
              </Link>
            </li>

            {/* Spacer */}
            <li className="pb-6"></li>

            {/* Companies */}
            <li>
              <Link href="/companies" className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md">
                <svg className="w-4 h-4 mr-3" fill="currentColor" viewBox="0 0 18 18">
                  <path d="M10 16v-4H8v4H2V4c0-1.1.9-2 2-2h6c1.09 0 2 .91 2 2v2h2c1.09 0 2 .91 2 2v8zM4 4v2h2V4zm0 4v2h2V8zm4-4v2h2V4zm0 4v2h2V8zm-4 4v2h2v-2zm8 0v2h2v-2zm0-4v2h2V8z"/>
                </svg>
                Companies
              </Link>
            </li>

            {/* Collectives Section */}
            <li className="pt-8">
              <div className="flex items-center justify-between px-3 mb-4">
                <span className="text-xs font-bold text-gray-600 uppercase">Collectives</span>
                <button className="text-gray-400 hover:text-gray-600">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 14 14">
                    <path d="M8 2H6v4H2v2h4v4h2V8h4V6H8z"/>
                  </svg>
                </button>
              </div>
              <p className="px-3 text-xs text-gray-500 mb-4">
                Communities for your favorite technologies. 
                <Link href="/collectives" className="text-blue-600 hover:underline font-medium ml-1">
                  Explore all Collectives
                </Link>
              </p>
            </li>
          </ul>
        </nav>

        {/* Teams Section */}
        <div className="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <button className="absolute top-2 right-2 text-gray-400 hover:text-gray-600">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 14 14">
              <path d="M12 3.41 10.59 2 7 5.59 3.41 2 2 3.41 5.59 7 2 10.59 3.41 12 7 8.41 10.59 12 12 10.59 8.41 7z"/>
            </svg>
          </button>
          
          <div className="text-xs font-bold text-gray-600 uppercase mb-3">Teams</div>
          
          <div className="mb-4">
            <img src="/api/placeholder/151/24" alt="Teams" className="mb-3 mx-auto" />
            <p className="text-xs text-gray-600 mb-3">
              Ask questions, find answers and collaborate at work with Stack Overflow for Teams.
            </p>
            <Link href="/teams/create" className="block w-full text-center px-3 py-2 text-xs font-medium text-white bg-orange-500 hover:bg-orange-600 rounded mb-2">
              Try Teams for free
            </Link>
            <Link href="/teams" className="block w-full text-center px-3 py-2 text-xs font-medium text-gray-700 border border-gray-300 hover:bg-gray-50 rounded">
              Explore Teams
            </Link>
          </div>
        </div>

        {/* Teams Migration Notice */}
        <div className="mt-4 px-3">
          <p className="text-xs text-gray-500">
            Looking for 
            <button className="text-blue-600 hover:underline font-medium">
              your Teams?
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LeftSidebar;
