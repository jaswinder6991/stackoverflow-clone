'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '@/services/api';

interface User {
  id: number;
  name: string;
  email: string;
  reputation?: number;
  badges?: {
    gold: number;
    silver: number;
    bronze: number;
  };
  profile?: {
    basic?: {
      displayName?: string;
      location?: string;
      title?: string;
      pronouns?: string;
    };
    about?: {
      bio?: string;
      interests?: string;
    };
    developer?: {
      primaryLanguage?: string;
      technologies?: string;
      yearsOfExperience?: string;
      githubProfile?: string;
    };
    work?: {
      currentPosition?: string;
      company?: string;
      startDate?: string;
      endDate?: string;
      description?: string;
    };
    education?: {
      institution?: string;
      degree?: string;
      fieldOfStudy?: string;
      graduationYear?: string;
    };
    links?: {
      website?: string;
      twitter?: string;
      linkedin?: string;
      github?: string;
    };
    preferences?: {
      emailNotifications?: boolean;
      publicProfile?: boolean;
      showDeveloperStory?: boolean;
      showActivityFeed?: boolean;
    };
  };
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (profileData: any) => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const response = await apiService.getCurrentUser();
      if (response.data) {
        setUser(response.data as User);
      }
    } catch (error) {
      console.error('Error refreshing user data:', error);
    }
  };

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      console.log('Checking authentication status...');
      try {
        const response = await apiService.getCurrentUser();
        console.log('getCurrentUser response:', response);
        if (response.data) {
          console.log('Setting user from /me endpoint:', response.data);
          setUser(response.data as User);
        }
      } catch (error) {
        // Only log errors that aren't 401 Unauthorized
        if (error instanceof Error) {
          try {
            const errorData = JSON.parse(error.message);
            if (errorData.status !== 401) {
              console.error('Auth check failed:', error);
            }
          } catch {
            console.error('Auth check failed:', error);
          }
        }
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    console.log('Attempting login for username:', username);
    const response = await apiService.login({ username, password });
    console.log('Login response:', response);
    
    if (response.error) {
      console.error('Login error:', response.error);
      throw new Error(response.error);
    }
    
    // After successful login, fetch user data
    try {
      const userResponse = await apiService.getCurrentUser();
      if (userResponse.data) {
        console.log('Setting user after successful login:', userResponse.data);
        setUser(userResponse.data as User);
      } else {
        console.warn('User data not found after login');
        throw new Error('Failed to fetch user data after login');
      }
    } catch (error) {
      console.error('Error fetching user data after login:', error);
      throw new Error('Failed to fetch user data after login');
    }
  };

  const register = async (username: string, email: string, password: string) => {
    console.log('Attempting registration for username:', username);
    const response = await apiService.register({ username, email, password });
    console.log('Registration response:', response);
    
    if (response.error) {
      console.error('Registration error:', response.error);
      throw new Error(response.error);
    }
    
    if (response.data) {
      console.log('Setting user after successful registration:', response.data);
      setUser(response.data as User);
    } else {
      console.warn('Registration response has no data:', response);
    }
  };

  const updateUser = async (profileData: any) => {
    console.log('Updating user profile:', profileData);
    if (!user?.id) {
      throw new Error('No user logged in');
    }
    try {
      const response = await apiService.updateProfile(profileData, user.id);
      if (response.data) {
        console.log('Profile updated successfully:', response.data);
        setUser(prev => prev ? { ...prev, profile: response.data as User['profile'] } : null);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      throw new Error('Failed to update profile');
    }
  };

  const logout = async () => {
    console.log('Logging out...');
    await apiService.logout();
    setUser(null);
    console.log('User logged out, user state cleared');
  };

  // Debug: Log user state changes
  useEffect(() => {
    console.log('Current user state:', user);
  }, [user]);

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 