"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useState } from "react";

// Simple SVG icons for Help and Logout
function HelpIcon() {
  return (
    <svg className="w-6 h-6 text-gray-600 hover:text-black" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
      <path d="M9.09 9a3 3 0 1 1 5.83 1c0 2-3 3-3 3" stroke="currentColor" strokeWidth="2" fill="none" />
      <circle cx="12" cy="17" r="1" fill="currentColor" />
    </svg>
  );
}
function LogoutIcon() {
  return (
    <svg className="w-6 h-6 text-gray-600 hover:text-black" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path d="M17 16l4-4m0 0l-4-4m4 4H7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3 12a9 9 0 1 1 18 0 9 9 0 0 1-18 0z" stroke="currentColor" strokeWidth="2" fill="none" />
    </svg>
  );
}

export default function TopNav() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [search, setSearch] = useState("");

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="flex items-center justify-between px-4 py-2 max-w-7xl mx-auto">
        {/* Left: Logo and Nav Links */}
        <div className="flex items-center space-x-6">
          <Link href="/" className="flex items-center">
            <span className="text-orange-500 font-bold text-2xl tracking-tight">stack<span className="text-black">overflow</span></span>
          </Link>
          <nav className="hidden md:flex items-center space-x-4 text-sm">
            <Link href="#" className="text-gray-700 hover:text-black">About</Link>
            <Link href="#" className="text-gray-700 hover:text-black">Products</Link>
            <Link href="#" className="text-gray-700 hover:text-black">For Teams</Link>
            <Link href="#" className="text-gray-700 hover:text-black">OverflowAI</Link>
          </nav>
        </div>
        {/* Center: Search Bar */}
        <div className="flex-1 max-w-xl mx-4">
          <form onSubmit={e => { e.preventDefault(); router.push(`/search?q=${encodeURIComponent(search)}`); }}>
            <div className="relative">
              <input
                type="text"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
              <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 18 18">
                <path d="m18 16.5-5.14-5.18h-.35a7 7 0 1 0-1.19 1.19v.35L16.5 18zM12 7A5 5 0 1 1 2 7a5 5 0 0 1 10 0"/>
              </svg>
            </div>
          </form>
        </div>
        {/* Right: Auth/User */}
        <div className="flex items-center space-x-4">
          {!user ? (
            <>
              <Link href="/auth/login" className="px-4 py-1 text-sm text-blue-600 border border-blue-600 rounded hover:bg-blue-50">Log in</Link>
              <Link href="/auth/register" className="px-4 py-1 text-sm text-white bg-blue-600 rounded hover:bg-blue-700">Sign up</Link>
            </>
          ) : (
            <>
              <Link href={`/users/${user.id}`} className="flex items-center px-2 py-1 hover:bg-gray-100 rounded" title="Profile">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  {user?.name?.charAt(0)?.toUpperCase() || "U"}
                </div>
              </Link>
              <Link href="/help" className="p-1" title="Help">
                <HelpIcon />
              </Link>
              <button
                onClick={handleLogout}
                className="p-1 rounded hover:bg-gray-100"
                title="Log out"
              >
                <LogoutIcon />
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
} 