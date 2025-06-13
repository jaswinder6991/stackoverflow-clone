import React from 'react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-16">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Stack Overflow */}
          <div>
            <h3 className="font-bold text-lg mb-4">STACK OVERFLOW</h3>
            <ul className="space-y-2">
              <li><Link href="/questions" className="text-gray-300 hover:text-white text-sm">Questions</Link></li>
              <li><Link href="/jobs" className="text-gray-300 hover:text-white text-sm">Jobs</Link></li>
              <li><Link href="/developer-survey" className="text-gray-300 hover:text-white text-sm">Developer Survey</Link></li>
            </ul>
          </div>

          {/* Products */}
          <div>
            <h3 className="font-bold text-lg mb-4">PRODUCTS</h3>
            <ul className="space-y-2">
              <li><Link href="/teams" className="text-gray-300 hover:text-white text-sm">Teams</Link></li>
              <li><Link href="/advertising" className="text-gray-300 hover:text-white text-sm">Advertising</Link></li>
              <li><Link href="/collectives" className="text-gray-300 hover:text-white text-sm">Collectives</Link></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-bold text-lg mb-4">COMPANY</h3>
            <ul className="space-y-2">
              <li><Link href="/about" className="text-gray-300 hover:text-white text-sm">About</Link></li>
              <li><Link href="/press" className="text-gray-300 hover:text-white text-sm">Press</Link></li>
              <li><Link href="/work-here" className="text-gray-300 hover:text-white text-sm">Work Here</Link></li>
            </ul>
          </div>

          {/* Network */}
          <div>
            <h3 className="font-bold text-lg mb-4">STACK EXCHANGE NETWORK</h3>
            <ul className="space-y-2">
              <li><Link href="/technology" className="text-gray-300 hover:text-white text-sm">Technology</Link></li>
              <li><Link href="/culture" className="text-gray-300 hover:text-white text-sm">Culture & recreation</Link></li>
              <li><Link href="/life" className="text-gray-300 hover:text-white text-sm">Life & arts</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <div className="text-orange-500 font-bold text-xl">Stack Overflow</div>
            <span className="text-gray-400 text-sm">Clone for educational purposes</span>
          </div>
          
          <div className="flex space-x-4 text-sm text-gray-400">
            <Link href="/terms" className="hover:text-white">Terms of service</Link>
            <Link href="/privacy" className="hover:text-white">Privacy policy</Link>
            <Link href="/cookie" className="hover:text-white">Cookie policy</Link>
          </div>
        </div>
        
        <div className="text-center mt-4 text-xs text-gray-500">
          <p>Built with Next.js, TypeScript, and Tailwind CSS</p>
        </div>
      </div>
    </footer>
  );
}
