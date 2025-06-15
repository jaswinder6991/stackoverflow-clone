'use client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

interface BackendQuestion {
  id: number;
  title: string;
  body: string;
  author_id: number;
  created_at: string;
  updated_at: string;
  votes: number;
  views: number;
  is_answered: boolean;
}

class ApiService {
  private static instance: ApiService;
  private baseUrl: string;
  private token: string | null;

  private constructor() {
    this.baseUrl = API_URL;
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private setToken(token: string | null) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      console.log(`Making API request to ${endpoint}`, { options });
      
      const headers = new Headers({
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string>),
      });

      // Add authorization header if token exists
      if (this.token) {
        headers.append('Authorization', `Bearer ${this.token}`);
      }

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include',
      });

      const data = await response.json();
      console.log(`API response from ${endpoint}:`, { status: response.status, data });

      // Special handling for /me endpoint - don't treat 401 as an error
      if (endpoint === '/auth/me' && response.status === 401) {
        this.setToken(null); // Clear token on 401
        return { data: undefined };
      }

      if (!response.ok) {
        // Clear token on any auth error
        if (response.status === 401) {
          this.setToken(null);
        }
        // Pass through the error details from the backend
        throw new Error(JSON.stringify({
          status: response.status,
          detail: data.detail
        }));
      }

      return { data };
    } catch (error) {
      console.error(`API request to ${endpoint} failed:`, error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Login now stores the token
  async login(credentials: { username: string; password: string }) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await this.request<{ access_token: string; token_type: string }>('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });

    if (response.data?.access_token) {
      this.setToken(response.data.access_token);
    }

    return response;
  }

  // Logout clears the token
  async logout() {
    const response = await this.request('/auth/logout', {
      method: 'POST',
    });
    this.setToken(null);
    return response;
  }

  // Questions
  async getQuestions() {
    return this.request('/questions');
  }

  async getQuestion(id: number) {
    return this.request<BackendQuestion>(`/questions/${id}`);
  }

  async createQuestion(data: { title: string; body: string; tags: string[]; author_id: number }) {
    // Data is already in the format expected by the backend
    const backendData = {
      title: data.title,
      body: data.body,
      author_id: data.author_id,
      tags: data.tags
    };

    return this.request('/questions', {
      method: 'POST',
      body: JSON.stringify(backendData),
    });
  }

  // Tags
  async getTags() {
    return this.request('/api/tags');
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

  async updateProfile(profileData: any, userId: number) {
    return this.request(`/api/users/${userId}/profile`, {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  // Authentication
  async register(userData: { username: string; email: string; password: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // Search
  async search(query: string) {
    return this.request(`/search?q=${encodeURIComponent(query)}`);
  }

  // Answers
  async createAnswer(data: { question_id: number; user_id: number; body: string }) {
    return this.request('/answers/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Voting
  async voteQuestion(questionId: number, userId: number, voteType: 'up' | 'down', isUndo: boolean = false) {
    // If this is undoing a vote, we use the opposite vote type to cancel it out
    const effectiveVoteType = isUndo 
      ? (voteType === 'up' ? 'down' : 'up') 
      : voteType;
      
    return this.request(`/questions/${questionId}/vote?user_id=${userId}&vote_type=${effectiveVoteType}`, {
      method: 'POST',
    });
  }

  async voteAnswer(answerId: number, userId: number, voteType: 'up' | 'down', isUndo: boolean = false) {
    // If this is undoing a vote, we use the opposite vote type to cancel it out
    const effectiveVoteType = isUndo 
      ? (voteType === 'up' ? 'down' : 'up') 
      : voteType;
      
    return this.request(`/answers/${answerId}/vote?user_id=${userId}&vote_type=${effectiveVoteType}`, {
      method: 'POST',
    });
  }
}

const apiService = ApiService.getInstance();
export default apiService;