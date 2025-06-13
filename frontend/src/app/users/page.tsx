import Image from 'next/image';

export default function UsersPage() {
  const topUsers = [
    {
      name: 'Jon Skeet',
      reputation: '1,234,567',
      avatar: 'https://www.gravatar.com/avatar/sample1?s=64&d=identicon&r=PG',
      location: 'Reading, United Kingdom',
      badges: { gold: 856, silver: 8946, bronze: 9284 },
      topTags: ['c#', '.net', 'java']
    },
    {
      name: 'Gordon Linoff',
      reputation: '987,654',
      avatar: 'https://www.gravatar.com/avatar/sample2?s=64&d=identicon&r=PG',
      location: 'New York, NY',
      badges: { gold: 456, silver: 5432, bronze: 6789 },
      topTags: ['sql', 'mysql', 'postgresql']
    },
    {
      name: 'VonC',
      reputation: '876,543',
      avatar: 'https://www.gravatar.com/avatar/sample3?s=64&d=identicon&r=PG',
      location: 'France',
      badges: { gold: 234, silver: 3456, bronze: 4567 },
      topTags: ['git', 'version-control', 'bash']
    },
    {
      name: 'Darin Dimitrov',
      reputation: '765,432',
      avatar: 'https://www.gravatar.com/avatar/sample4?s=64&d=identicon&r=PG',
      location: 'Bulgaria',
      badges: { gold: 345, silver: 4567, bronze: 5678 },
      topTags: ['asp.net-mvc', 'c#', 'javascript']
    },
  ];

  return (
    <div className="p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Users</h1>
        
        <div className="flex justify-between items-center mb-6">
          <div className="flex space-x-4">
            <button className="px-4 py-2 bg-orange-500 text-white rounded">Reputation</button>
            <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">New users</button>
            <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">Voters</button>
            <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">Editors</button>
          </div>
          <input
            type="text"
            placeholder="Filter by user"
            className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {topUsers.map((user) => (
            <div key={user.name} className="bg-white border border-gray-300 rounded p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center space-x-3 mb-3">
                <Image
                  src={user.avatar}
                  alt={`${user.name}'s avatar`}
                  width={48}
                  height={48}
                  className="rounded"
                />
                <div>
                  <h3 className="font-medium text-blue-600 hover:text-blue-800 cursor-pointer">
                    {user.name}
                  </h3>
                  <p className="text-sm text-gray-600">{user.location}</p>
                </div>
              </div>
              
              <div className="mb-3">
                <div className="text-lg font-semibold text-gray-800">{user.reputation}</div>
                <div className="text-xs text-gray-600 flex items-center space-x-2">
                  <span className="text-yellow-600">●</span>
                  <span>{user.badges.gold}</span>
                  <span className="text-gray-500">●</span>
                  <span>{user.badges.silver}</span>
                  <span className="text-orange-600">●</span>
                  <span>{user.badges.bronze}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1">
                {user.topTags.map((tag) => (
                  <span
                    key={tag}
                    className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs"
                  >
                    {tag}
                  </span>
                ))}
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
