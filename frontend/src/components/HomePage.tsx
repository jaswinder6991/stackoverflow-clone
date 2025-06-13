import React from 'react';
import Layout from './Layout';
import MainContent from './MainContent';
import Navigation from '@/components/Navigation';
import { useAuth } from '@/contexts/AuthContext';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <Layout>
      <Navigation />
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Welcome to Stack Overflow
            </h1>
            <p className="text-lg text-gray-600 mb-6">
              A synthetic website for testing and development purposes.
            </p>
            {user ? (
              <p className="text-gray-600">
                Welcome back, {user.username}! You can now browse questions, tags, and users.
              </p>
            ) : (
              <p className="text-gray-600">
                Please{' '}
                <a href="/auth/login" className="text-blue-500 hover:text-blue-600">
                  login
                </a>{' '}
                or{' '}
                <a href="/auth/register" className="text-blue-500 hover:text-blue-600">
                  register
                </a>{' '}
                to get started.
              </p>
            )}
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default HomePage;
