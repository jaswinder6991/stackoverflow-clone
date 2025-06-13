'use client';

import React, { useState } from 'react';
import { Search, Menu, Inbox, Trophy, MessageSquare, HelpCircle } from 'lucide-react';
import Image from 'next/image';
import MobileSidebar from './MobileSidebar';
import Sidebar from './Sidebar';

export default function Header() {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  return (
    <>
      <header className="bg-white border-b border-gray-300 shadow-sm sticky top-0 z-50">
        <div className="flex items-center justify-between px-4 py-2 max-w-7xl mx-auto">
          {/* Left side - Logo and Navigation */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <button 
              className="md:hidden"
              onClick={() => setIsMobileSidebarOpen(true)}
            >
              <Menu className="w-6 h-6 text-gray-600" />
            </button>
            
            {/* Logo */}
            <div className="flex items-center">
              <div className="text-orange-500 font-bold text-xl">
                Stack Overflow
              </div>
            </div>

            {/* Desktop navigation */}
            <nav className="hidden md:flex space-x-1">
              <button className="px-3 py-2 text-gray-600 hover:bg-gray-100 rounded">
                Products
              </button>
            </nav>
          </div>

          {/* Search bar */}
          <div className="flex-1 max-w-2xl mx-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Right side - User actions */}
          <div className="flex items-center space-x-2">
            {/* User profile */}
            <div className="flex items-center space-x-2 px-3 py-1 hover:bg-gray-100 rounded cursor-pointer">
              <Image
                src="https://i.sstatic.net/9qF7N.jpg?s=32"
                alt="User avatar"
                width={24}
                height={24}
                className="rounded"
              />
              <span className="hidden sm:inline text-sm text-gray-700">2,584</span>
              <div className="hidden sm:flex items-center space-x-1">
                <span className="text-yellow-600">●</span>
                <span className="text-xs">2</span>
                <span className="text-gray-500">●</span>
                <span className="text-xs">23</span>
                <span className="text-orange-600">●</span>
                <span className="text-xs">25</span>
              </div>
            </div>

            {/* Inbox */}
            <button className="p-2 hover:bg-gray-100 rounded relative">
              <Inbox className="w-5 h-5 text-gray-600" />
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
                2
              </span>
            </button>

            {/* Achievements */}
            <button className="p-2 hover:bg-gray-100 rounded">
              <Trophy className="w-5 h-5 text-gray-600" />
            </button>

            {/* Review */}
            <button className="p-2 hover:bg-gray-100 rounded relative">
              <MessageSquare className="w-5 h-5 text-gray-600" />
              <span className="absolute -top-1 -right-1 bg-red-500 w-2 h-2 rounded-full"></span>
            </button>

            {/* Help */}
            <button className="p-2 hover:bg-gray-100 rounded">
              <HelpCircle className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>
      </header>
      
      {/* Mobile Sidebar */}
      <MobileSidebar 
        isOpen={isMobileSidebarOpen} 
        onClose={() => setIsMobileSidebarOpen(false)}
      >
        <Sidebar />
      </MobileSidebar>
    </>
  );
}
