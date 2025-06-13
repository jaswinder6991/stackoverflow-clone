import React from 'react';
import Link from 'next/link';

const RightSidebar = () => {
  return (
    <div className="w-80 flex-shrink-0">
      <div className="sticky top-20 space-y-6">
        {/* The Overflow Blog Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">The Overflow Blog</h3>
          </div>
          <div className="p-4">
            <ul className="space-y-3">
              <li className="flex items-start space-x-2">
                <svg className="w-4 h-4 mt-0.5 text-gray-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Better vibes and vibe coding with Gemini 2.5
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Featured on Meta Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Featured on Meta</h3>
          </div>
          <div className="p-4">
            <ul className="space-y-3">
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-gray-300 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  How Can We Bring More Fun to the Stack Ecosystem? Community Ideas Welcome!
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-gray-300 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Thoughts on the future of Stack Exchange site customisation
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-orange-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  How can I revert the style/layout changes to comments?
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-orange-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Policy: Generative AI (e.g., ChatGPT) is banned
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-orange-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Experimenting with the Commenting Reputation Requirement
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-orange-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  2025 Community Moderator Election Results
                </Link>
              </li>
            </ul>
          </div>
          
          {/* Hot Meta Posts Section */}
          <div className="border-t border-gray-200">
            <div className="px-4 py-3">
              <h4 className="text-sm font-semibold text-gray-900">Hot Meta Posts</h4>
            </div>
            <div className="px-4 pb-4">
              <ul className="space-y-3">
                <li className="flex items-start space-x-2">
                  <div className="w-4 h-4 mt-0.5 bg-orange-500 rounded-sm flex-shrink-0"></div>
                  <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                    Finally hanging up my diamond(s)
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Recently Viewed Posts Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Recently viewed posts</h3>
          </div>
          <div className="p-4">
            <ul className="space-y-4">
              <li>
                <Link href="#" className="block">
                  <h4 className="text-sm font-medium text-gray-900 hover:text-blue-600">
                    What are the differences between Servlet 2.5 and 3?
                  </h4>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-xs text-gray-500">
                      99 votes • 4 answers
                    </div>
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      + Follow
                    </button>
                  </div>
                </Link>
              </li>
              <li>
                <Link href="#" className="block">
                  <h4 className="text-sm font-medium text-gray-900 hover:text-blue-600">
                    Is java Purely Object Oriented?
                  </h4>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-xs text-gray-500">
                      8 votes • 11 answers
                    </div>
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      + Follow
                    </button>
                  </div>
                </Link>
              </li>
              <li>
                <Link href="#" className="block">
                  <h4 className="text-sm font-medium text-gray-900 hover:text-blue-600">
                    How to implement pagination in Spring Boot
                  </h4>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-xs text-gray-500">
                      45 votes • 7 answers
                    </div>
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      + Follow
                    </button>
                  </div>
                </Link>
              </li>
              <li>
                <Link href="#" className="block">
                  <h4 className="text-sm font-medium text-gray-900 hover:text-blue-600">
                    Understanding React useEffect hook
                  </h4>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-xs text-gray-500">
                      23 votes • 3 answers
                    </div>
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      + Follow
                    </button>
                  </div>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Custom Interest Tags Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Watched Tags</h3>
          </div>
          <div className="p-4">
            <div className="flex flex-wrap gap-2 mb-4">
              <Link href="/questions/tagged/javascript" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200">
                javascript
              </Link>
              <Link href="/questions/tagged/react" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200">
                react
              </Link>
              <Link href="/questions/tagged/typescript" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200">
                typescript
              </Link>
              <Link href="/questions/tagged/node.js" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200">
                node.js
              </Link>
              <Link href="/questions/tagged/python" className="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-md hover:bg-blue-200">
                python
              </Link>
            </div>
            <Link href="/users/tag-preferences" className="text-xs text-blue-600 hover:text-blue-800">
              Edit watched tags
            </Link>
          </div>
        </div>

        {/* Hot Network Questions Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Hot Network Questions</h3>
          </div>
          <div className="p-4">
            <ul className="space-y-3">
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-red-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Why does my code work in development but not in production?
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-green-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Best practices for REST API design
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-blue-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  How to handle authentication in microservices
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-purple-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Understanding async/await in JavaScript
                </Link>
              </li>
              <li className="flex items-start space-x-2">
                <div className="w-4 h-4 mt-0.5 bg-yellow-500 rounded-sm flex-shrink-0"></div>
                <Link href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Docker vs Kubernetes: When to use what?
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Community Stats Widget */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-4 py-3 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900">Stack Overflow Stats</h3>
          </div>
          <div className="p-4">
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-lg font-bold text-gray-900">24.2M+</div>
                <div className="text-xs text-gray-500">questions</div>
              </div>
              <div>
                <div className="text-lg font-bold text-gray-900">35.8M+</div>
                <div className="text-xs text-gray-500">answers</div>
              </div>
              <div>
                <div className="text-lg font-bold text-gray-900">22.1M+</div>
                <div className="text-xs text-gray-500">users</div>
              </div>
              <div>
                <div className="text-lg font-bold text-gray-900">8,975</div>
                <div className="text-xs text-gray-500">questions today</div>
              </div>
            </div>
          </div>
        </div>

        {/* Advertisement Placeholder */}
        <div className="bg-gray-100 border border-gray-200 rounded-lg p-8 text-center">
          <div className="text-xs text-gray-500 mb-2">Advertisement</div>
          <div className="w-full h-32 bg-gray-200 rounded flex items-center justify-center">
            <span className="text-gray-400 text-sm">Ad Space</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RightSidebar;
