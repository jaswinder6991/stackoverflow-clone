'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '@/services/api';

interface User {
  id: number;
  username: string;
  email: string;
  reputation?: number;
  badges?: {
    gold: number;
    silver: number;
    bronze: number;
  };
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      try {
        const response = await apiService.getCurrentUser();
        if (response.data) {
          setUser(response.data as User);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    const response = await apiService.login({ username, password });
    if (response.error) {
      throw new Error(response.error);
    }
    if (response.data) {
      setUser(response.data as User);
    }
  };

  const register = async (username: string, email: string, password: string) => {
    const response = await apiService.register({ username, email, password });
    if (response.error) {
      throw new Error(response.error);
    }
    if (response.data) {
      setUser(response.data as User);
    }
  };

  const logout = async () => {
    await apiService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
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