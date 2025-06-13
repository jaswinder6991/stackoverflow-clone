import React from 'react';
import { Home } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export default function Sidebar() {
  return (
    <aside className="hidden md:block w-64 bg-white border-r border-gray-300 min-h-screen p-4">
      <nav className="space-y-2">
        {/* Main Navigation */}
        <div className="space-y-1">
          <Link href="/" className="flex items-center space-x-3 px-2 py-2 text-gray-700 hover:bg-gray-100 rounded">
            <Home className="w-4 h-4" />
            <span>Home</span>
          </Link>
          
          <div className="ml-6 space-y-1">          <Link href="/questions" className="block px-2 py-1 text-sm text-gray-600 hover:text-orange-600">
            Questions
          </Link>
          <Link href="/tags" className="block px-2 py-1 text-sm text-gray-600 hover:text-orange-600">
            Tags
          </Link>
          <Link href="/users" className="block px-2 py-1 text-sm text-gray-600 hover:text-orange-600">
            Users
          </Link>
          </div>
        </div>

        {/* Collectives */}
        <div className="pt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-gray-500 uppercase">Collectives</span>
            <button className="text-gray-400 hover:text-gray-600">
              <span className="text-xs">+</span>
            </button>
          </div>
          <p className="text-xs text-gray-500 mb-2 px-2">
            Communities for your favorite technologies.{' '}
            <Link href="/collectives" className="text-blue-600 hover:underline">
              Explore all Collectives
            </Link>
          </p>
        </div>

        {/* Teams */}
        <div className="pt-4 bg-blue-50 rounded p-3 mt-4">
          <div className="text-xs font-semibold text-gray-700 mb-2">TEAMS</div>
          <div className="mb-3">
            <Image 
              src="/api/placeholder/150/24" 
              alt="Teams promo" 
              width={150}
              height={24}
              className="w-full h-6 object-contain mb-2"
            />
            <p className="text-xs text-gray-600 mb-3">
              Ask questions, find answers and collaborate at work with Stack Overflow for Teams.
            </p>
            <button className="w-full bg-orange-500 text-white text-xs py-2 px-3 rounded hover:bg-orange-600 mb-2">
              Try Teams for free
            </button>
            <button className="w-full border border-gray-300 text-gray-700 text-xs py-2 px-3 rounded hover:bg-gray-50">
              Explore Teams
            </button>
          </div>
        </div>
      </nav>
    </aside>
  );
}
