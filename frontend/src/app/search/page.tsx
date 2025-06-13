export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const params = await searchParams;
  const query = params.q || '';

  // Mock search results
  const searchResults = [
    {
      id: 1,
      title: "How to implement authentication in React?",
      excerpt: "I'm trying to add user authentication to my React app. What are the best practices?",
      votes: 15,
      answers: 3,
      views: 1234,
      tags: ["react", "authentication", "javascript"],
      author: "john_dev",
      asked: "2 hours ago"
    },
    {
      id: 2,
      title: "Next.js API routes vs Express.js",
      excerpt: "What are the differences between Next.js API routes and traditional Express.js?",
      votes: 8,
      answers: 2,
      views: 567,
      tags: ["nextjs", "express", "api"],
      author: "web_developer",
      asked: "5 hours ago"
    },
    {
      id: 3,
      title: "TypeScript generic constraints",
      excerpt: "How do I properly use generic constraints in TypeScript?",
      votes: 12,
      answers: 4,
      views: 890,
      tags: ["typescript", "generics"],
      author: "ts_expert",
      asked: "1 day ago"
    }
  ];

  return (
    <div className="p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">
            {query ? `Search Results for "${query}"` : 'Search'}
          </h1>
          {query && (
            <p className="text-gray-600">
              Found {searchResults.length} results
            </p>
          )}
        </div>

        {query ? (
          <div className="space-y-4">
            {searchResults.map((result) => (
              <div key={result.id} className="bg-white border border-gray-300 rounded p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-3">
                  <h2 className="text-lg font-medium text-blue-600 hover:text-blue-800 cursor-pointer">
                    {result.title}
                  </h2>
                  <div className="flex space-x-4 text-sm text-gray-600">
                    <span>{result.votes} votes</span>
                    <span>{result.answers} answers</span>
                    <span>{result.views} views</span>
                  </div>
                </div>
                <p className="text-gray-700 mb-3">{result.excerpt}</p>
                <div className="flex items-center justify-between">
                  <div className="flex space-x-2">
                    {result.tags.map((tag) => (
                      <span
                        key={tag}
                        className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="text-sm text-gray-600">
                    asked {result.asked} by <span className="text-blue-600">{result.author}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">Enter a search term to find questions</p>
            <div className="max-w-md mx-auto">
              <input
                type="text"
                placeholder="Search for questions..."
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
