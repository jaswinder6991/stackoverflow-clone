#!/usr/bin/env python3
"""
Test script to create a new question and answer
"""
import requests
import json

def create_question_and_answer():
    print('Creating a new question...')
    question_data = {
        'title': 'How to implement user authentication in a React application with TypeScript?',
        'body': 'I am building a React application using TypeScript and need to implement user authentication. What are the best practices for handling login, logout, and protecting routes? Should I use JWT tokens, session-based authentication, or something else? Any code examples would be greatly appreciated.',
        'author_id': 1,
        'tags': ['react', 'typescript', 'authentication', 'security']
    }

    try:
        response = requests.post('http://localhost:8000/questions/', json=question_data)
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            result = response.json()
            print(f'✓ Question created successfully!')
            print(f'  Question ID: {result["id"]}')
            print(f'  Title: {result["title"]}')
            print(f'  Author ID: {result["author_id"]}')
            print(f'  Created: {result["created_at"]}')
            question_id = result["id"]
            
            # Now create an answer for this question
            print(f"\nCreating an answer for question {question_id}...")
            answer_data = {
                'question_id': question_id,
                'user_id': 2,
                'body': '''Here's a comprehensive approach to implementing authentication in React with TypeScript:

## 1. Choose Your Authentication Strategy

**JWT (JSON Web Tokens)** is recommended for modern React applications:

```typescript
// types/auth.ts
export interface User {
  id: number;
  email: string;
  name: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}
```

## 2. Create an Auth Context

```typescript
// contexts/AuthContext.tsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.token);
        dispatch({ type: 'LOGIN_SUCCESS', payload: data });
      }
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Login failed' });
    }
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

## 3. Protected Routes

```typescript
// components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};
```

## 4. API Interceptors

```typescript
// utils/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

This approach provides secure, scalable authentication with proper TypeScript support.'''
            }
            
            answer_response = requests.post('http://localhost:8000/answers/', json=answer_data)
            print(f'Answer Status: {answer_response.status_code}')
            if answer_response.status_code == 200:
                answer_result = answer_response.json()
                print(f'✓ Answer created successfully!')
                print(f'  Answer ID: {answer_result["id"]}')
                print(f'  Content length: {len(answer_result["body"])} characters')
                
                print(f'\n🎉 Success! Visit http://localhost:3000/questions/{question_id} to see the new question and answer!')
                return question_id
            else:
                print(f'✗ Answer creation failed: {answer_response.text}')
                
        else:
            print(f'✗ Question creation failed: {response.text}')
    except Exception as e:
        print(f'Error: {e}')
        return None

if __name__ == "__main__":
    create_question_and_answer()
