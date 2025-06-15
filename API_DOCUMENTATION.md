# API Documentation

## Authentication Endpoints

Base URL: `http://localhost:8000`

### Overview
The authentication system uses JWT (JSON Web Tokens) for securing API endpoints. Users must register and login to receive an access token, which should be included in the `Authorization` header as `Bearer <token>` for protected endpoints.

### Security Configuration
- **Algorithm**: HS256
- **Token Expiration**: 30 minutes
- **Password Hashing**: bcrypt

---

## 1. User Registration

**Endpoint**: `POST /auth/register`

**Description**: Register a new user account.

**Authentication**: None required

### Request Body
```json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

### Request Example
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Response

#### Success (201 Created)
```json
{
  "id": 1,
  "name": "johndoe",
  "email": "john@example.com",
  "reputation": 0,
  "location": null,
  "website": null,
  "is_active": true,
  "profile": null,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Error Responses

**400 Bad Request - Username Already Exists**
```json
{
  "detail": {
    "error": "Username already registered",
    "field": "username", 
    "message": "The username 'johndoe' is already taken"
  }
}
```

**400 Bad Request - Email Already Exists**
```json
{
  "detail": {
    "error": "Email already registered",
    "field": "email",
    "message": "The email 'john@example.com' is already registered"
  }
}
```

**500 Internal Server Error**
```json
{
  "detail": {
    "error": "Registration failed",
    "message": "An unexpected error occurred during registration. Please try again."
  }
}
```

---

## 2. User Login

**Endpoint**: `POST /auth/login`

**Description**: Authenticate user and receive access token.

**Authentication**: None required

**Content-Type**: `application/x-www-form-urlencoded`

### Request Body (Form Data)
```
username=johndoe
password=securepassword123
```

### Request Example
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

### Response

#### Success (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Error Responses

**401 Unauthorized - User Not Found**
```json
{
  "detail": {
    "error": "User not found",
    "message": "No account found with username 'johndoe'. Please register first."
  }
}
```

**401 Unauthorized - Invalid Password**
```json
{
  "detail": {
    "error": "Invalid password", 
    "message": "The password you entered is incorrect. Please try again."
  }
}
```

---

## 3. Get Current User

**Endpoint**: `GET /auth/me`

**Description**: Get information about the currently authenticated user.

**Authentication**: Bearer token required

### Request Headers
```
Authorization: Bearer <access_token>
```

### Request Example
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Response

#### Success (200 OK)
```json
{
  "id": 1,
  "name": "johndoe",
  "email": "john@example.com", 
  "reputation": 150,
  "location": "New York, NY",
  "website": "https://johndoe.com",
  "is_active": true,
  "profile": {
    "bio": "Software developer passionate about web technologies",
    "links": {
      "website": "https://johndoe.com",
      "twitter": "@johndoe",
      "github": "johndoe"
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Error Responses

**401 Unauthorized - Invalid/Missing Token**
```json
{
  "detail": "Could not validate credentials"
}
```

**401 Unauthorized - Token Expired**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## Authentication Flow

### 1. Register New User
```javascript
// Register
POST /auth/register
{
  "username": "newuser",
  "email": "user@example.com", 
  "password": "password123"
}

// Response: User object with user details
```

### 2. Login and Get Token
```javascript
// Login
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=newuser&password=password123

// Response: 
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Use Token for Protected Endpoints
```javascript
// Use token in Authorization header
GET /auth/me
Authorization: Bearer jwt_token_here

// All other protected endpoints require this header
```

---

## Error Handling

All authentication endpoints follow consistent error response formats:

### HTTP Status Codes
- `200` - Success
- `201` - Created (registration)
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication failed)
- `500` - Internal Server Error

### Error Response Format
```json
{
  "detail": {
    "error": "error_type",
    "field": "field_name", // Optional, for validation errors
    "message": "Human readable error message"
  }
}
```


## Testing Examples

### Complete Authentication Flow Test
```bash
# 1. Register a user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123"}'

# 2. Login to get token  
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123" | jq -r '.access_token')

# 3. Use token to get user info
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

# Answer Endpoints

## Overview
Answer endpoints manage answers to questions. Users can create, read, update, delete answers, and vote on them. Most endpoints require authentication via Bearer token.

---

## 1. Get Answers

**Endpoint**: `GET /answers/`

**Description**: Retrieve answers with optional filtering and pagination.

**Authentication**: None required

### Query Parameters
- `question_id` (optional, integer): Filter answers by question ID
- `user_id` (optional, integer): Filter answers by user ID  
- `page` (integer, default=1): Page number (≥1)
- `limit` (integer, default=20): Results per page (1-100)
- `sort` (string, default="votes"): Sort by "votes", "newest", or "oldest"

### Request Example
```bash
# Get all answers
curl -X GET "http://localhost:8000/answers/"

# Get answers for specific question with pagination
curl -X GET "http://localhost:8000/answers/?question_id=5&page=1&limit=10&sort=votes"

# Get all answers by specific user
curl -X GET "http://localhost:8000/answers/?user_id=2&sort=newest"
```

### Response

#### Success (200 OK)
```json
[
  {
    "id": 1,
    "body": "This is a comprehensive answer to the question...",
    "question_id": 5,
    "author_id": 2,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "votes": 12,
    "is_accepted": false
  },
  {
    "id": 2,
    "body": "Another helpful answer with code examples...",
    "question_id": 5,
    "author_id": 3,
    "created_at": "2024-01-15T11:45:00Z",
    "updated_at": "2024-01-15T11:45:00Z",
    "votes": 8,
    "is_accepted": true
  }
]
```

---

## 2. Get Single Answer

**Endpoint**: `GET /answers/{answer_id}`

**Description**: Retrieve a specific answer by ID.

**Authentication**: None required

### Path Parameters
- `answer_id` (integer, required): The ID of the answer to retrieve

### Request Example
```bash
curl -X GET "http://localhost:8000/answers/1"
```

### Response

#### Success (200 OK)
```json
{
  "id": 1,
  "body": "This is a comprehensive answer to the question...",
  "question_id": 5,
  "author_id": 2,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "votes": 12,
  "is_accepted": false
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Answer not found"
}
```

---

## 3. Create Answer

**Endpoint**: `POST /answers/`

**Description**: Create a new answer to a question.

**Authentication**: Bearer token required

### Request Body
```json
{
  "body": "string (required)",
  "question_id": "integer (required)",
  "user_id": "integer (required)"
}
```

### Request Example
```bash
curl -X POST "http://localhost:8000/answers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "Here is my detailed answer with code examples and explanations...",
    "question_id": 5,
    "user_id": 2
  }'
```

### Response

#### Success (201 Created)
```json
{
  "id": 15,
  "body": "Here is my detailed answer with code examples and explanations...",
  "question_id": 5,
  "author_id": 2,
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-15T14:20:00Z",
  "votes": 0,
  "is_accepted": false
}
```

#### Error Responses

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "body"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 4. Update Answer

**Endpoint**: `PUT /answers/{answer_id}`

**Description**: Update an existing answer.

**Authentication**: Bearer token required

### Path Parameters
- `answer_id` (integer, required): The ID of the answer to update

### Request Body
```json
{
  "body": "string (required)"
}
```

### Request Example
```bash
curl -X PUT "http://localhost:8000/answers/15" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "Updated answer with additional information and corrections..."
  }'
```

### Response

#### Success (200 OK)
```json
{
  "id": 15,
  "body": "Updated answer with additional information and corrections...",
  "question_id": 5,
  "author_id": 2,
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-15T15:30:00Z",
  "votes": 3,
  "is_accepted": false
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Answer not found"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 5. Delete Answer

**Endpoint**: `DELETE /answers/{answer_id}`

**Description**: Delete an existing answer.

**Authentication**: Bearer token required

### Path Parameters
- `answer_id` (integer, required): The ID of the answer to delete

### Request Example
```bash
curl -X DELETE "http://localhost:8000/answers/15" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "Answer deleted successfully"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Answer not found"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 6. Vote on Answer

**Endpoint**: `POST /answers/{answer_id}/vote`

**Description**: Vote up or down on an answer, or remove a previous vote.

**Authentication**: Bearer token required

### Path Parameters  
- `answer_id` (integer, required): The ID of the answer to vote on

### Query Parameters
- `user_id` (integer, required): The ID of the user casting the vote
- `vote_type` (string, required): Either "up" or "down"
- `undo` (boolean, default=false): Set to true to remove the vote instead of adding it

### Request Example
```bash
# Vote up on an answer
curl -X POST "http://localhost:8000/answers/15/vote?user_id=2&vote_type=up" \
  -H "Authorization: Bearer $TOKEN"

# Vote down on an answer  
curl -X POST "http://localhost:8000/answers/15/vote?user_id=2&vote_type=down" \
  -H "Authorization: Bearer $TOKEN"

# Remove a previous vote
curl -X POST "http://localhost:8000/answers/15/vote?user_id=2&vote_type=up&undo=true" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "Vote recorded successfully"
}
```

```json
{
  "message": "Vote removed successfully"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Answer not found"
}
```

**400 Bad Request - Invalid Vote Type**
```json
{
  "detail": "Invalid vote type"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 7. Get User Vote on Answer

**Endpoint**: `GET /answers/{answer_id}/user_vote`

**Description**: Get the current user's vote on a specific answer.

**Authentication**: Bearer token required

### Path Parameters
- `answer_id` (integer, required): The ID of the answer

### Query Parameters  
- `user_id` (integer, required): The ID of the user to check vote for

### Request Example
```bash
curl -X GET "http://localhost:8000/answers/15/user_vote?user_id=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "vote": "up"
}
```

```json
{
  "vote": "down"
}
```

```json
{
  "vote": null
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Answer not found"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## Answer Data Model

### Answer Object
```json
{
  "id": "integer (unique identifier)",
  "body": "string (answer content)",
  "question_id": "integer (ID of the question this answers)",
  "author_id": "integer (ID of the user who wrote the answer)",
  "created_at": "datetime (ISO 8601 format)",
  "updated_at": "datetime (ISO 8601 format)",
  "votes": "integer (net vote score)",
  "is_accepted": "boolean (whether this is the accepted answer)"
}
```

### AnswerCreate Object
```json
{
  "body": "string (required - answer content)",
  "question_id": "integer (required - ID of question to answer)",
  "user_id": "integer (required - ID of user creating the answer)"
}
```

### AnswerUpdate Object
```json
{
  "body": "string (required - updated answer content)"
}
```

---

## Complete Answer Workflow Example

```bash
# 1. Get authentication token (see auth section)
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123" | jq -r '.access_token')

# 2. Create a new answer
ANSWER_ID=$(curl -X POST "http://localhost:8000/answers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "This is my comprehensive answer...",
    "question_id": 5,
    "user_id": 2
  }' | jq -r '.id')

# 3. Vote on the answer
curl -X POST "http://localhost:8000/answers/$ANSWER_ID/vote?user_id=3&vote_type=up" \
  -H "Authorization: Bearer $TOKEN"

# 4. Check user's vote
curl -X GET "http://localhost:8000/answers/$ANSWER_ID/user_vote?user_id=3" \
  -H "Authorization: Bearer $TOKEN"

# 5. Update the answer
curl -X PUT "http://localhost:8000/answers/$ANSWER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"body": "Updated answer with more details..."}'

# 6. Get all answers for the question
curl -X GET "http://localhost:8000/answers/?question_id=5&sort=votes"
```

---

# Question Endpoints

## Overview
Question endpoints manage the core Q&A functionality. Users can create, read, update, delete questions, search for questions, vote on them, and filter by various criteria.

---

## 1. Get Questions

**Endpoint**: `GET /questions/`

**Description**: Retrieve questions with optional filtering, sorting, and pagination.

**Authentication**: None required

### Query Parameters
- `skip` (integer, default=0): Number of questions to skip (≥0)
- `limit` (integer, default=15): Number of questions to return (1-100)
- `sort` (string, default="newest"): Sort by "newest", "votes", or "active"
- `tag` (optional, string): Filter by specific tag
- `user_id` (optional, integer): Filter by user ID

### Request Example
```bash
# Get all questions with default pagination
curl -X GET "http://localhost:8000/questions/"

# Get questions with custom pagination and sorting
curl -X GET "http://localhost:8000/questions/?skip=20&limit=10&sort=votes"

# Get questions by specific user
curl -X GET "http://localhost:8000/questions/?user_id=5&limit=20"

# Get questions by tag
curl -X GET "http://localhost:8000/questions/?tag=python&sort=newest"
```

### Response

#### Success (200 OK)
```json
{
  "items": [
    {
      "id": 1,
      "title": "How to implement authentication in FastAPI?",
      "content": "I'm looking for a comprehensive guide on implementing JWT authentication...",
      "author": {
        "name": "johndoe",
        "email": "john@example.com",
        "reputation": 150,
        "avatar": "",
        "location": "New York, NY",
        "website": "https://johndoe.com",
        "is_active": true,
        "profile": null
      },
      "tags": ["fastapi", "authentication", "jwt"],
      "votes": 12,
      "views": 245,
      "answer_count": 3,
      "asked": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 15
}
```

---

## 2. Search Questions

**Endpoint**: `GET /questions/search`

**Description**: Search questions by text query with optional filtering.

**Authentication**: None required

### Query Parameters
- `q` (string, required): Search query text
- `tags` (optional, array): Filter by tags
- `skip` (integer, default=0): Number of results to skip
- `limit` (integer, default=15): Number of results to return (1-100)
- `sort` (string, default="relevance"): Sort by "relevance", "newest", "votes", or "active"

### Request Example
```bash
# Basic search
curl -X GET "http://localhost:8000/questions/search?q=authentication"

# Search with tag filtering
curl -X GET "http://localhost:8000/questions/search?q=database&tags=python&tags=sql"

# Search with pagination and sorting
curl -X GET "http://localhost:8000/questions/search?q=fastapi&sort=votes&skip=10&limit=5"
```

### Response

#### Success (200 OK)
```json
[
  {
    "id": 1,
    "title": "How to implement authentication in FastAPI?",
    "content": "I'm looking for a comprehensive guide on implementing JWT authentication...",
    "author": {
      "name": "johndoe",
      "email": "john@example.com",
      "reputation": 150,
      "avatar": "",
      "location": null,
      "website": null,
      "is_active": true,
      "profile": null
    },
    "tags": ["fastapi", "authentication", "jwt"],
    "votes": 12,
    "views": 245,
    "answer_count": 3,
    "asked": "2024-01-15T10:30:00Z"
  }
]
```

---

## 3. Get Single Question

**Endpoint**: `GET /questions/{question_id}`

**Description**: Retrieve a specific question by ID with full details and answers.

**Authentication**: None required

### Path Parameters
- `question_id` (integer, required): The ID of the question to retrieve

### Request Example
```bash
curl -X GET "http://localhost:8000/questions/1"
```

### Response

#### Success (200 OK)
```json
{
  "id": 1,
  "title": "How to implement authentication in FastAPI?",
  "body": "I'm looking for a comprehensive guide on implementing JWT authentication in FastAPI. What are the best practices?",
  "author_id": 5,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "votes": 12,
  "views": 246,
  "is_answered": true
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Question not found"
}
```

---

## 4. Create Question

**Endpoint**: `POST /questions/`

**Description**: Create a new question.

**Authentication**: Bearer token required

### Request Body
```json
{
  "title": "string (required)",
  "body": "string (required)",
  "author_id": "integer (required)",
  "tags": ["string"] // optional array
}
```

### Request Example
```bash
curl -X POST "http://localhost:8000/questions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "How to optimize database queries in Django?",
    "body": "I have a Django application with performance issues. The database queries are taking too long. What are the best practices for optimization?",
    "author_id": 5,
    "tags": ["django", "database", "optimization"]
  }'
```

### Response

#### Success (201 Created)
```json
{
  "id": 25,
  "title": "How to optimize database queries in Django?",
  "body": "I have a Django application with performance issues...",
  "author_id": 5,
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-15T14:20:00Z",
  "votes": 0,
  "views": 1,
  "is_answered": false
}
```

#### Error Responses

**404 Not Found - User Not Found**
```json
{
  "detail": "User not found"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 5. Update Question

**Endpoint**: `PUT /questions/{question_id}`

**Description**: Update an existing question.

**Authentication**: Bearer token required

### Path Parameters
- `question_id` (integer, required): The ID of the question to update

### Request Body
```json
{
  "title": "string (required)",
  "body": "string (required)"
}
```

### Request Example
```bash
curl -X PUT "http://localhost:8000/questions/25" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "How to optimize database queries in Django? [Updated]",
    "body": "I have a Django application with performance issues. Updated with more specific details about the problem..."
  }'
```

### Response

#### Success (200 OK)
```json
{
  "id": 25,
  "title": "How to optimize database queries in Django? [Updated]",
  "body": "I have a Django application with performance issues. Updated with more specific details...",
  "author_id": 5,
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-15T15:45:00Z",
  "votes": 2,
  "views": 15,
  "is_answered": false
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Question not found"
}
```

---

## 6. Delete Question

**Endpoint**: `DELETE /questions/{question_id}`

**Description**: Delete an existing question.

**Authentication**: Bearer token required

### Path Parameters
- `question_id` (integer, required): The ID of the question to delete

### Request Example
```bash
curl -X DELETE "http://localhost:8000/questions/25" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "Question 25 would be deleted",
  "success": true
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Question not found"
}
```

---

## 7. Vote on Question

**Endpoint**: `POST /questions/{question_id}/vote`

**Description**: Vote up or down on a question, or remove a previous vote.

**Authentication**: Bearer token required

### Path Parameters
- `question_id` (integer, required): The ID of the question to vote on

### Query Parameters
- `user_id` (integer, required): The ID of the user casting the vote
- `vote_type` (string, required): Either "up" or "down"
- `undo` (boolean, default=false): Set to true to remove the vote instead of adding it

### Request Example
```bash
# Vote up on a question
curl -X POST "http://localhost:8000/questions/25/vote?user_id=2&vote_type=up" \
  -H "Authorization: Bearer $TOKEN"

# Remove a previous vote
curl -X POST "http://localhost:8000/questions/25/vote?user_id=2&vote_type=up&undo=true" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "Vote recorded successfully"
}
```

```json
{
  "message": "Vote removed successfully"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "Question not found"
}
```

**400 Bad Request**
```json
{
  "detail": "Invalid vote type"
}
```

---

## 8. Get Questions by Tag

**Endpoint**: `GET /questions/tagged/{tag}`

**Description**: Get questions filtered by a specific tag.

**Authentication**: None required

### Path Parameters
- `tag` (string, required): The tag to filter by

### Query Parameters
- `skip` (integer, default=0): Number of questions to skip
- `limit` (integer, default=15): Number of questions to return (1-100)
- `sort` (string, default="newest"): Sort by "newest", "votes", or "active"

### Request Example
```bash
curl -X GET "http://localhost:8000/questions/tagged/python?limit=10&sort=votes"
```

### Response

#### Success (200 OK)
```json
[
  {
    "id": 1,
    "title": "Python list comprehension best practices",
    "content": "What are the best practices when using list comprehensions...",
    "author": {
      "name": "pythondev",
      "email": "dev@example.com",
      "reputation": 200,
      "avatar": "",
      "location": null,
      "website": null,
      "is_active": true,
      "profile": null
    },
    "tags": ["python", "best-practices"],
    "votes": 25,
    "views": 480,
    "answer_count": 5,
    "asked": "2024-01-10T09:15:00Z"
  }
]
```

---

## 9. Get User Vote on Question

**Endpoint**: `GET /questions/{question_id}/user_vote`

**Description**: Get the current user's vote on a specific question.

**Authentication**: Bearer token required

### Path Parameters
- `question_id` (integer, required): The ID of the question

### Query Parameters
- `user_id` (integer, required): The ID of the user to check vote for

### Request Example
```bash
curl -X GET "http://localhost:8000/questions/25/user_vote?user_id=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "vote": "up"
}
```

```json
{
  "vote": null
}
```

---

## 10. Get User Votes on Question and Answers

**Endpoint**: `GET /questions/{question_id}/user_votes`

**Description**: Get user's votes on a question and all its answers.

**Authentication**: Bearer token required

### Path Parameters
- `question_id` (integer, required): The ID of the question

### Query Parameters
- `user_id` (integer, required): The ID of the user to check votes for

### Request Example
```bash
curl -X GET "http://localhost:8000/questions/25/user_votes?user_id=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "question_vote": "up",
  "answer_votes": {
    "15": "up",
    "16": null,
    "17": "down"
  }
}
```

---

# Comment Endpoints

## Overview
Comment endpoints manage comments on questions and answers. Users can create comments, retrieve comments, and vote on them.

---

## 1. Create Comment

**Endpoint**: `POST /comments/`

**Description**: Create a new comment on a question or answer.

**Authentication**: Bearer token required

### Request Body
```json
{
  "body": "string (required, 15-1000 characters)",
  "question_id": "integer (optional)",
  "answer_id": "integer (optional)", 
  "author_id": "integer (required)"
}
```

**Note**: Either `question_id` OR `answer_id` must be provided, not both.

### Request Example
```bash
# Comment on a question
curl -X POST "http://localhost:8000/comments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "Great question! I had the same issue recently.",
    "question_id": 25,
    "author_id": 3
  }'

# Comment on an answer
curl -X POST "http://localhost:8000/comments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "This solution worked perfectly for me, thanks!",
    "answer_id": 15,
    "author_id": 3
  }'
```

### Response

#### Success (201 Created)
```json
{
  "id": 45,
  "body": "Great question! I had the same issue recently.",
  "author_id": 3,
  "question_id": 25,
  "answer_id": null,
  "created_at": "2024-01-15T16:20:00Z",
  "updated_at": "2024-01-15T16:20:00Z",
  "votes": 0
}
```

#### Error Responses

**404 Not Found - User Not Found**
```json
{
  "detail": "User not found"
}
```

**400 Bad Request - Validation Error**
```json
{
  "detail": "Comment must be associated with either a question or an answer"
}
```

---

## 2. Get Question Comments

**Endpoint**: `GET /comments/question/{question_id}`

**Description**: Retrieve all comments for a specific question.

**Authentication**: None required

### Path Parameters
- `question_id` (integer, required): The ID of the question

### Request Example
```bash
curl -X GET "http://localhost:8000/comments/question/25"
```

### Response

#### Success (200 OK)
```json
[
  {
    "id": 45,
    "body": "Great question! I had the same issue recently.",
    "author_id": 3,
    "question_id": 25,
    "answer_id": null,
    "created_at": "2024-01-15T16:20:00Z",
    "updated_at": "2024-01-15T16:20:00Z",
    "votes": 2
  },
  {
    "id": 46,
    "body": "Have you tried checking the documentation?",
    "author_id": 7,
    "question_id": 25,
    "answer_id": null,
    "created_at": "2024-01-15T17:10:00Z",
    "updated_at": "2024-01-15T17:10:00Z",
    "votes": 0
  }
]
```

---

## 3. Get Answer Comments

**Endpoint**: `GET /comments/answer/{answer_id}`

**Description**: Retrieve all comments for a specific answer.

**Authentication**: None required

### Path Parameters
- `answer_id` (integer, required): The ID of the answer

### Request Example
```bash
curl -X GET "http://localhost:8000/comments/answer/15"
```

### Response

#### Success (200 OK)
```json
[
  {
    "id": 47,
    "body": "This solution worked perfectly for me, thanks!",
    "author_id": 3,
    "question_id": null,
    "answer_id": 15,
    "created_at": "2024-01-15T18:30:00Z",
    "updated_at": "2024-01-15T18:30:00Z",
    "votes": 5
  }
]
```

---

## 4. Vote on Comment

**Endpoint**: `POST /comments/{comment_id}/vote`

**Description**: Vote on a comment (upvote only, toggle to remove).

**Authentication**: Bearer token required

### Path Parameters
- `comment_id` (integer, required): The ID of the comment to vote on

### Query Parameters
- `user_id` (integer, required): The ID of the user casting the vote

### Request Example
```bash
# Vote on a comment (toggle vote)
curl -X POST "http://localhost:8000/comments/45/vote?user_id=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "Comment vote toggled successfully"
}
```

#### Error Responses

**404 Not Found - User Not Found**
```json
{
  "detail": "User not found"
}
```

**404 Not Found - Comment Not Found**
```json
{
  "detail": "Comment not found"
}
```

---

## 5. Get Comment Vote Status

**Endpoint**: `GET /comments/{comment_id}/vote-status/{user_id}`

**Description**: Get user's vote status for a comment.

**Authentication**: Bearer token required

### Path Parameters
- `comment_id` (integer, required): The ID of the comment
- `user_id` (integer, required): The ID of the user

### Request Example
```bash
curl -X GET "http://localhost:8000/comments/45/vote-status/2" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "has_voted": true
}
```

```json
{
  "has_voted": false
}
```

---

# User Endpoints

## Overview
User endpoints manage user accounts, profiles, and user-related data. Users can be retrieved, updated, and their statistics can be accessed.

---

## 1. Get Users

**Endpoint**: `GET /api/users/`

**Description**: Retrieve users with pagination and optional search.

**Authentication**: None required

### Query Parameters
- `page` (integer, default=1): Page number (≥1)
- `limit` (integer, default=20): Number of users to return (1-100)
- `search` (optional, string): Search users by name or location

### Request Example
```bash
# Get all users with default pagination
curl -X GET "http://localhost:8000/api/users/"

# Get users with custom pagination
curl -X GET "http://localhost:8000/api/users/?page=2&limit=10"

# Search users
curl -X GET "http://localhost:8000/api/users/?search=john&limit=5"
```

### Response

#### Success (200 OK)
```json
{
  "items": [
    {
      "id": 1,
      "name": "johndoe",
      "email": "john@example.com",
      "reputation": 150,
      "avatar": "",
      "location": "New York, NY",
      "website": "https://johndoe.com",
      "is_active": true,
      "profile": {
        "basic": {
          "displayName": "John Doe",
          "location": "New York, NY",
          "title": "Software Developer"
        },
        "about": {
          "bio": "Passionate about web development"
        }
      },
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20
}
```

---

## 2. Get Single User

**Endpoint**: `GET /api/users/{user_id}`

**Description**: Retrieve a specific user by ID.

**Authentication**: None required

### Path Parameters
- `user_id` (integer, required): The ID of the user to retrieve

### Request Example
```bash
curl -X GET "http://localhost:8000/api/users/1"
```

### Response

#### Success (200 OK)
```json
{
  "id": 1,
  "name": "johndoe",
  "email": "john@example.com",
  "reputation": 150,
  "avatar": "",
  "location": "New York, NY",
  "website": "https://johndoe.com",
  "is_active": true,
  "profile": {
    "basic": {
      "displayName": "John Doe",
      "location": "New York, NY",
      "title": "Software Developer"
    },
    "about": {
      "bio": "Passionate about web development"
    },
    "links": {
      "website": "https://johndoe.com",
      "twitter": "@johndoe",
      "github": "johndoe"
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

---

## 3. Get User Questions

**Endpoint**: `GET /api/users/{user_id}/questions`

**Description**: Get questions posted by a specific user.

**Authentication**: None required

### Path Parameters
- `user_id` (integer, required): The ID of the user

### Query Parameters
- `page` (integer, default=1): Page number (≥1)
- `limit` (integer, default=20): Number of questions to return (1-100)

### Request Example
```bash
curl -X GET "http://localhost:8000/api/users/1/questions?page=1&limit=10"
```

### Response

#### Success (200 OK)
```json
{
  "items": [
    {
      "id": 25,
      "title": "How to optimize database queries in Django?",
      "body": "I have a Django application with performance issues...",
      "author_id": 1,
      "created_at": "2024-01-15T14:20:00Z",
      "updated_at": "2024-01-15T14:20:00Z",
      "votes": 12,
      "views": 245,
      "is_answered": true
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 10
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

---

## 4. Get User Answers

**Endpoint**: `GET /api/users/{user_id}/answers`

**Description**: Get answers posted by a specific user.

**Authentication**: None required

### Path Parameters
- `user_id` (integer, required): The ID of the user

### Query Parameters
- `page` (integer, default=1): Page number (≥1)
- `limit` (integer, default=20): Number of answers to return (1-100)

### Request Example
```bash
curl -X GET "http://localhost:8000/api/users/1/answers?page=1&limit=10"
```

### Response

#### Success (200 OK)
```json
{
  "items": [
    {
      "id": 15,
      "body": "Here's a comprehensive solution to your problem...",
      "question_id": 5,
      "author_id": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "votes": 8,
      "is_accepted": true
    }
  ],
  "total": 12,
  "page": 1,
  "limit": 10
}
```

---

## 5. Get User Statistics

**Endpoint**: `GET /api/users/{user_id}/stats`

**Description**: Get statistics for a specific user.

**Authentication**: None required

### Path Parameters
- `user_id` (integer, required): The ID of the user

### Request Example
```bash
curl -X GET "http://localhost:8000/api/users/1/stats"
```

### Response

#### Success (200 OK)
```json
{
  "total_questions": 5,
  "total_answers": 12,
  "total_votes": 45,
  "reputation": 150,
  "badges": {
    "gold": 1,
    "silver": 3,
    "bronze": 8
  }
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

---

## 6. Create User

**Endpoint**: `POST /api/users/`

**Description**: Create a new user account.

**Authentication**: Bearer token required

### Request Body
```json
{
  "name": "string (required, 3-50 characters)",
  "email": "string (required, valid email)",
  "password": "string (required)"
}
```

### Request Example
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123"
  }'
```

### Response

#### Success (201 Created)
```json
{
  "id": 50,
  "name": "newuser",
  "email": "newuser@example.com",
  "reputation": 0,
  "avatar": "",
  "location": null,
  "website": null,
  "is_active": true,
  "profile": null,
  "created_at": "2024-01-15T20:00:00Z",
  "updated_at": "2024-01-15T20:00:00Z"
}
```

---

## 7. Update User

**Endpoint**: `PUT /api/users/{user_id}`

**Description**: Update user information.

**Authentication**: Bearer token required

### Path Parameters
- `user_id` (integer, required): The ID of the user to update

### Request Body
```json
{
  "name": "string (optional)",
  "email": "string (optional, valid email)",
  "is_active": "boolean (optional)"
}
```

### Request Example
```bash
curl -X PUT "http://localhost:8000/api/users/50" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "updateduser",
    "email": "updated@example.com"
  }'
```

### Response

#### Success (200 OK)
```json
{
  "id": 50,
  "name": "updateduser",
  "email": "updated@example.com",
  "reputation": 0,
  "avatar": "",
  "location": null,
  "website": null,
  "is_active": true,
  "profile": null,
  "created_at": "2024-01-15T20:00:00Z",
  "updated_at": "2024-01-15T20:15:00Z"
}
```

---

## 8. Update User Profile

**Endpoint**: `PUT /api/users/{user_id}/profile`

**Description**: Update user's profile information.

**Authentication**: Bearer token required

### Path Parameters
- `user_id` (integer, required): The ID of the user

### Request Body
```json
{
  "basic": {
    "displayName": "string",
    "location": "string",
    "title": "string",
    "pronouns": "string"
  },
  "about": {
    "bio": "string",
    "interests": "string"
  },
  "developer": {
    "primaryLanguage": "string",
    "technologies": "string",
    "yearsOfExperience": "string",
    "githubProfile": "string"
  },
  "links": {
    "website": "string",
    "twitter": "string",
    "github": "string"
  }
}
```

### Request Example
```bash
curl -X PUT "http://localhost:8000/api/users/1/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "basic": {
      "displayName": "John Doe",
      "location": "San Francisco, CA",
      "title": "Senior Software Engineer"
    },
    "about": {
      "bio": "Passionate full-stack developer with 5+ years experience"
    },
    "links": {
      "website": "https://johndoe.dev",
      "twitter": "@johndoe",
      "github": "johndoe"
    }
  }'
```

### Response

#### Success (200 OK)
```json
{
  "id": 1,
  "name": "johndoe",
  "email": "john@example.com",
  "reputation": 150,
  "avatar": "",
  "location": "San Francisco, CA",
  "website": "https://johndoe.dev",
  "is_active": true,
  "profile": {
    "basic": {
      "displayName": "John Doe",
      "location": "San Francisco, CA",
      "title": "Senior Software Engineer"
    },
    "about": {
      "bio": "Passionate full-stack developer with 5+ years experience"
    },
    "links": {
      "website": "https://johndoe.dev",
      "twitter": "@johndoe",
      "github": "johndoe"
    }
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-15T21:00:00Z"
}
```

---

## 9. Delete User

**Endpoint**: `DELETE /api/users/{user_id}`

**Description**: Delete a user account.

**Authentication**: Bearer token required

### Path Parameters
- `user_id` (integer, required): The ID of the user to delete

### Request Example
```bash
curl -X DELETE "http://localhost:8000/api/users/50" \
  -H "Authorization: Bearer $TOKEN"
```

### Response

#### Success (200 OK)
```json
{
  "message": "User deleted successfully"
}
```

#### Error Responses

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

---

## Complete API Workflow Examples

### Question Creation and Management Workflow
```bash
# 1. Login and get token
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123" | jq -r '.access_token')

# 2. Create a question
QUESTION_ID=$(curl -X POST "http://localhost:8000/questions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "How to use FastAPI with PostgreSQL?",
    "body": "I need help connecting FastAPI to PostgreSQL database...",
    "author_id": 1,
    "tags": ["fastapi", "postgresql", "python"]
  }' | jq -r '.id')

# 3. Create an answer to the question
ANSWER_ID=$(curl -X POST "http://localhost:8000/answers/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "Here is how you can connect FastAPI to PostgreSQL...",
    "question_id": '$QUESTION_ID',
    "user_id": 2
  }' | jq -r '.id')

# 4. Add a comment to the question
curl -X POST "http://localhost:8000/comments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "body": "Great question! I was wondering the same thing.",
    "question_id": '$QUESTION_ID',
    "author_id": 3
  }'

# 5. Vote on the question and answer
curl -X POST "http://localhost:8000/questions/$QUESTION_ID/vote?user_id=4&vote_type=up" \
  -H "Authorization: Bearer $TOKEN"

curl -X POST "http://localhost:8000/answers/$ANSWER_ID/vote?user_id=4&vote_type=up" \
  -H "Authorization: Bearer $TOKEN"

# 6. Search for similar questions
curl -X GET "http://localhost:8000/questions/search?q=FastAPI%20PostgreSQL&sort=votes"
``` 