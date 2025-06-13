"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

const TopBar = () => {
  const [isProductsOpen, setIsProductsOpen] = useState(false);
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const [isSitesSwitcherOpen, setIsSitesSwitcherOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex items-center h-12 px-3">
        {/* Mobile menu button */}
        <button className="p-2 mr-2 md:hidden hover:bg-gray-100 rounded">
          <span className="block w-4 h-0.5 bg-gray-600 mb-1"></span>
          <span className="block w-4 h-0.5 bg-gray-600 mb-1"></span>
          <span className="block w-4 h-0.5 bg-gray-600"></span>
        </button>

        {/* Logo */}
        <Link href="/" className="flex items-center mr-4">
          <span className="text-xl font-bold text-gray-800">Stack Overflow</span>
        </Link>

        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-1 mr-4">
          <div className="relative">
            <button 
              className="px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded"
              onClick={() => setIsProductsOpen(!isProductsOpen)}
            >
              Products
            </button>
            {isProductsOpen && (
              <div className="absolute top-full left-0 mt-1 w-80 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                <div className="p-4">
                  <Link href="#" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Stack Overflow for Teams</div>
                    <div className="text-xs text-gray-500 mt-1">Where developers & technologists share private knowledge with coworkers</div>
                  </Link>
                  <Link href="#" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Advertising</div>
                    <div className="text-xs text-gray-500 mt-1">Reach devs & technologists worldwide about your product, service or employer brand</div>
                  </Link>
                  <Link href="#" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Knowledge Solutions</div>
                    <div className="text-xs text-gray-500 mt-1">Data licensing offering for businesses to build and improve AI tools and models</div>
                  </Link>
                  <div className="border-t border-gray-200 mt-2 pt-2">
                    <Link href="#" className="block p-3 hover:bg-gray-50 rounded">
                      <div className="font-medium text-sm">Labs</div>
                      <div className="text-xs text-gray-500 mt-1">The future of collective knowledge sharing</div>
                    </Link>
                  </div>
                  <div className="bg-gray-50 border-t border-gray-200 mt-2 pt-2">
                    <Link href="#" className="block p-3 text-gray-600 hover:text-gray-800">About the company</Link>
                    <Link href="#" className="block p-3 text-gray-600 hover:text-gray-800">Visit the blog</Link>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <Link href="#" className="px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded md:hidden">
            OverflowAI
          </Link>
        </nav>

        {/* Search */}
        <div className="flex-1 max-w-md mx-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search…"
              className="w-full px-3 py-1 pl-8 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
            />
            <svg className="absolute left-2 top-1.5 w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 18 18">
              <path d="m18 16.5-5.14-5.18h-.35a7 7 0 1 0-1.19 1.19v.35L16.5 18zM12 7A5 5 0 1 1 2 7a5 5 0 0 1 10 0"/>
            </svg>
          </div>
        </div>

        {/* User Navigation */}
        <nav className="flex items-center space-x-1">
          {/* Search button (mobile) */}
          <button className="p-2 text-gray-600 hover:bg-gray-100 rounded sm:hidden">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 18 18">
              <path d="m18 16.5-5.14-5.18h-.35a7 7 0 1 0-1.19 1.19v.35L16.5 18zM12 7A5 5 0 1 1 2 7a5 5 0 0 1 10 0"/>
            </svg>
          </button>

          {/* User Profile */}
          <Link href="/users/profile" className="flex items-center px-2 py-1 text-sm hover:bg-gray-100 rounded">
            <div className="w-6 h-6 bg-blue-500 rounded mr-2">
              <Image src="/api/placeholder/24/24" alt="User avatar" width={24} height={24} className="rounded" />
            </div>
            <div className="hidden sm:block">
              <div className="text-xs text-gray-500">2,584</div>
              <div className="text-xs">
                <span className="text-yellow-600">●</span>2
                <span className="text-gray-400 ml-1">●</span>23
                <span className="text-orange-600 ml-1">●</span>25
              </div>
            </div>
          </Link>

          {/* Inbox */}
          <Link href="/inbox" className="relative p-2 text-gray-600 hover:bg-gray-100 rounded">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 18">
              <path d="M4.63 1h10.56a2 2 0 0 1 1.94 1.35L20 10.79V15a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-4.21l2.78-8.44c.25-.8 1-1.36 1.85-1.35m8.28 12 2-2h2.95l-2.44-7.32a1 1 0 0 0-.95-.68H5.35a1 1 0 0 0-.95.68L1.96 11h2.95l2 2z"/>
            </svg>
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">2</span>
          </Link>

          {/* Achievements */}
          <Link href="/achievements" className="p-2 text-gray-600 hover:bg-gray-100 rounded">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 18 18">
              <path d="M15 2V1H3v1H0v4c0 1.6 1.4 3 3 3v1c.4 1.5 3 2.6 5 3v2H5s-1 1.5-1 2h10c0-.4-1-2-1-2h-3v-2c2-.4 4.6-1.5 5-3V9c1.6-.2 3-1.4 3-3V2zM3 7c-.5 0-1-.5-1-1V4h1zm8.4 2.5L9 8 6.6 9.4l1-2.7L5 5h3l1-2.7L10 5h2.8l-2.3 1.8 1 2.7zM16 6c0 .5-.5 1-1 1V4h1z"/>
            </svg>
          </Link>

          {/* Review */}
          <Link href="/review" className="p-2 text-gray-600 hover:bg-gray-100 rounded">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 18 18">
              <path d="m11 12.47 5-4.97V3a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h6.5l-2.79-2.8a1 1 0 0 1 0-1.4l2.1-2.1a1 1 0 0 1 1.4 0zM2 7h10v2H2zm0-4h12v2H2zm0 10v-2h3v2zm9 4.5 7-7L16.5 9 11 14.5 8.5 12 7 13.5z"/>
            </svg>
          </Link>

          {/* Help */}
          <div className="relative">
            <button 
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              onClick={() => setIsHelpOpen(!isHelpOpen)}
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 18 18">
                <path d="M9 1C4.64 1 1 4.64 1 9s3.64 8 8 8 8-3.64 8-8-3.64-8-8-8m.81 12.13c-.02.71-.55 1.15-1.24 1.13-.66-.02-1.17-.49-1.15-1.2.02-.72.56-1.18 1.22-1.16.7.03 1.2.51 1.17 1.23M11.77 8c-.59.66-1.78 1.09-2.05 1.97a4 4 0 0 0-.09.75c0 .05-.03.16-.18.16H7.88c-.16 0-.18-.1-.18-.15.06-1.35.66-2.2 1.83-2.88.39-.29.7-.75.7-1.24.01-1.24-1.64-1.82-2.35-.72-.21.33-.18.73-.18 1.1H5.75c0-1.97 1.03-3.26 3.03-3.26 1.75 0 3.47.87 3.47 2.83 0 .57-.2 1.05-.48 1.44"/>
              </svg>
            </button>
            {isHelpOpen && (
              <div className="absolute top-full right-0 mt-1 w-72 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                <div className="p-4">
                  <Link href="/tour" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Tour</div>
                    <div className="text-xs text-gray-500 mt-1">Start here for a quick overview of the site</div>
                  </Link>
                  <Link href="/help" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Help Center</div>
                    <div className="text-xs text-gray-500 mt-1">Detailed answers to any questions you might have</div>
                  </Link>
                  <Link href="https://meta.stackoverflow.com" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">Meta</div>
                    <div className="text-xs text-gray-500 mt-1">Discuss the workings and policies of this site</div>
                  </Link>
                  <Link href="/about" className="block p-3 hover:bg-gray-50 rounded">
                    <div className="font-medium text-sm">About Us</div>
                    <div className="text-xs text-gray-500 mt-1">Learn more about Stack Overflow the company, and our products</div>
                  </Link>
                </div>
              </div>
            )}
          </div>

          {/* Site Switcher */}
          <div className="relative">
            <button 
              className="p-2 text-gray-600 hover:bg-gray-100 rounded"
              onClick={() => setIsSitesSwitcherOpen(!isSitesSwitcherOpen)}
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 18 18">
                <path d="M15 1H3a2 2 0 0 0-2 2v2h16V3a2 2 0 0 0-2-2M1 13c0 1.1.9 2 2 2h8v3l3-3h1a2 2 0 0 0 2-2v-2H1zm16-7H1v4h16z"/>
              </svg>
            </button>
            {isSitesSwitcherOpen && (
              <div className="absolute top-full right-0 mt-1 w-80 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                <div className="p-4">
                  <h3 className="font-medium text-sm mb-4">current community</h3>
                  <div className="flex items-center mb-4">
                    <div className="w-8 h-8 bg-orange-500 rounded mr-3"></div>
                    <div>
                      <div className="font-medium text-sm">Stack Overflow</div>
                      <div className="text-xs text-gray-500">2,584 reputation</div>
                    </div>
                  </div>
                  <h3 className="font-medium text-sm mb-2">your communities</h3>
                  <div className="space-y-2">
                    <Link href="#" className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-orange-500 rounded-sm mr-2"></div>
                        <span className="text-sm">Stack Overflow</span>
                      </div>
                      <span className="text-xs text-gray-500">2,584</span>
                    </Link>
                    <Link href="#" className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                      <div className="flex items-center">
                        <div className="w-4 h-4 bg-blue-500 rounded-sm mr-2"></div>
                        <span className="text-sm">Economics</span>
                      </div>
                      <span className="text-xs text-gray-500">373</span>
                    </Link>
                  </div>
                </div>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
};

export default TopBar;
