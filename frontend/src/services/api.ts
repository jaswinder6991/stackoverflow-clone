'use client';

import { analyticsLogger } from './analyticsLogger';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  private static instance: ApiService;
  private baseUrl: string;

  private constructor() {
    this.baseUrl = API_URL;
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
      };

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include',
      });

      const data = await response.json();

      if (!response.ok) {
        // Pass through the error details from the backend
        throw new Error(JSON.stringify({
          status: response.status,
          detail: data.detail
        }));
      }

      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Questions
  async getQuestions() {
    return this.request('/questions');
  }

  async getQuestion(id: number) {
    return this.request(`/questions/${id}`);
  }

  async createQuestion(data: { title: string; content: string; tags: string[] }) {
    return this.request('/questions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Tags
  async getTags() {
    return this.request('/tags');
  }

  async getTag(name: string) {
    return this.request(`/tags/${name}`);
  }

  // Users
  async getUsers() {
    return this.request('/users');
  }

  async getUser(id: number) {
    return this.request(`/users/${id}`);
  }

  // Authentication
  async login(credentials: { username: string; password: string }) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    return this.request('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });
  }

  async register(userData: { username: string; email: string; password: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  // Search
  async search(query: string) {
    return this.request(`/search?q=${encodeURIComponent(query)}`);
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }
}

const apiService = ApiService.getInstance();
export default apiService; 