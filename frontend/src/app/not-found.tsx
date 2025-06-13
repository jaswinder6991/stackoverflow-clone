import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8 text-center">
        <div className="mb-6">
          <h1 className="text-6xl font-bold text-gray-300 mb-2">404</h1>
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Page not found</h2>
          <p className="text-gray-600 mb-6">
            The page you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>
        </div>
        
        <div className="space-y-3">
          <Link 
            href="/"
            className="block w-full bg-orange-500 text-white py-2 px-4 rounded hover:bg-orange-600 transition-colors"
          >
            Go to Home
          </Link>
          <Link 
            href="/questions"
            className="block w-full border border-gray-300 text-gray-700 py-2 px-4 rounded hover:bg-gray-50 transition-colors"
          >
            Browse Questions
          </Link>
        </div>
        
        <div className="mt-8 text-sm text-gray-500">
          <p>Looking for something specific?</p>
          <Link href="/search" className="text-blue-600 hover:underline">
            Try searching
          </Link>
        </div>
      </div>
    </div>
  );
}
