export default function AskQuestionPage() {
  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Ask a public question</h1>
        
        <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-6">
          <h3 className="font-semibold text-blue-800 mb-2">Writing a good question</h3>
          <p className="text-blue-700 text-sm">
            You&apos;re ready to ask a programming-related question and this form will help guide you through the process.
            Looking to ask a non-programming question? See the topics here to find a relevant site.
          </p>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            <p className="text-sm text-gray-600 mb-2">
              Be specific and imagine you&apos;re asking a question to another person.
            </p>
            <input
              type="text"
              placeholder="e.g. Is there an R function for finding the index of an element in a vector?"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What are the details of your problem?
            </label>
            <p className="text-sm text-gray-600 mb-2">
              Introduce the problem and expand on what you put in the title. Minimum 20 characters.
            </p>
            <div className="border border-gray-300 rounded">
              <div className="bg-gray-100 px-3 py-2 border-b border-gray-300 flex space-x-2">
                <button className="px-2 py-1 bg-white border border-gray-300 rounded text-sm">B</button>
                <button className="px-2 py-1 bg-white border border-gray-300 rounded text-sm italic">I</button>
                <button className="px-2 py-1 bg-white border border-gray-300 rounded text-sm">Code</button>
                <button className="px-2 py-1 bg-white border border-gray-300 rounded text-sm">Link</button>
              </div>
              <textarea
                rows={10}
                placeholder="Enter your question details here..."
                className="w-full px-3 py-2 resize-none focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What did you try and what were you expecting?
            </label>
            <p className="text-sm text-gray-600 mb-2">
              Describe what you tried, what you expected to happen, and what actually resulted. Minimum 20 characters.
            </p>
            <textarea
              rows={6}
              placeholder="Describe what you've tried..."
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <p className="text-sm text-gray-600 mb-2">
              Add up to 5 tags to describe what your question is about. Start typing to see suggestions.
            </p>
            <input
              type="text"
              placeholder="e.g. (javascript typescript react)"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex space-x-4">
            <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
              Post your question
            </button>
            <button className="bg-white text-gray-700 px-6 py-2 border border-gray-300 rounded hover:bg-gray-50">
              Discard draft
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
