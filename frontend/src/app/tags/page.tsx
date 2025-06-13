export default function TagsPage() {
  const popularTags = [
    { name: 'javascript', count: '254,328', description: 'For questions about the JavaScript programming language' },
    { name: 'python', count: '198,745', description: 'For questions about the Python programming language' },
    { name: 'java', count: '178,623', description: 'For questions about the Java programming language' },
    { name: 'typescript', count: '156,789', description: 'For questions about TypeScript, a typed superset of JavaScript' },
    { name: 'react', count: '145,234', description: 'For questions about React, a JavaScript library for building user interfaces' },
    { name: 'nextjs', count: '89,456', description: 'For questions about Next.js, a React framework' },
    { name: 'nodejs', count: '123,567', description: 'For questions about Node.js, a JavaScript runtime' },
    { name: 'html', count: '87,345', description: 'For questions about HTML markup language' },
    { name: 'css', count: '76,234', description: 'For questions about CSS styling' },
    { name: 'sql', count: '65,123', description: 'For questions about SQL database queries' },
  ];

  return (
    <div className="p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Tags</h1>
        <p className="text-gray-600 mb-6">
          A tag is a keyword or label that categorizes your question with other, similar questions. 
          Using the right tags makes it easier for others to find and answer your question.
        </p>

        <div className="mb-6">
          <input
            type="text"
            placeholder="Filter by tag name"
            className="w-full max-w-md px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {popularTags.map((tag) => (
            <div key={tag.name} className="bg-white border border-gray-300 rounded p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-2">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-medium">
                  {tag.name}
                </span>
                <span className="text-gray-600 text-sm">{tag.count} questions</span>
              </div>
              <p className="text-gray-700 text-sm">{tag.description}</p>
              <div className="mt-3 flex justify-between text-xs text-gray-500">
                <span>Updated today</span>
                <span>Asked today</span>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-center mt-8">
          <div className="flex space-x-2">
            <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">Prev</button>
            <button className="px-3 py-2 bg-orange-500 text-white rounded">1</button>
            <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">2</button>
            <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">3</button>
            <button className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50">Next</button>
          </div>
        </div>
      </div>
    </div>
  );
}
