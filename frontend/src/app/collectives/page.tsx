import Image from 'next/image';

export default function CollectivesPage() {
  const collectives = [
    {
      name: 'Google Cloud',
      description: 'Google Cloud Collective on Stack Overflow',
      members: '12.5k',
      logo: '/api/placeholder/48/48',
      tags: ['google-cloud-platform', 'google-app-engine', 'google-cloud-functions']
    },
    {
      name: 'AWS',
      description: 'Amazon Web Services Collective',
      members: '15.2k',
      logo: '/api/placeholder/48/48',
      tags: ['amazon-web-services', 'aws-lambda', 'amazon-s3']
    },
    {
      name: 'Azure',
      description: 'Microsoft Azure Collective',
      members: '9.8k',
      logo: '/api/placeholder/48/48',
      tags: ['azure', 'azure-functions', 'azure-devops']
    },
  ];

  return (
    <div className="p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Collectives</h1>
        <p className="text-gray-600 mb-6">
          Find centralized, trusted content and collaborate around the technologies you use most.
        </p>

        <div className="space-y-4">
          {collectives.map((collective) => (
            <div key={collective.name} className="bg-white border border-gray-300 rounded p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start space-x-4">
                <Image
                  src={collective.logo}
                  alt={`${collective.name} logo`}
                  width={48}
                  height={48}
                  className="rounded"
                />
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-xl font-semibold text-blue-600 hover:text-blue-800 cursor-pointer">
                      {collective.name}
                    </h3>
                    <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs font-medium">
                      Collective
                    </span>
                  </div>
                  <p className="text-gray-700 mb-3">{collective.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex space-x-2">
                      {collective.tags.map((tag) => (
                        <span
                          key={tag}
                          className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                    <div className="text-sm text-gray-600">
                      {collective.members} members
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-8">
          <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
            View all Collectives
          </button>
        </div>
      </div>
    </div>
  );
}
