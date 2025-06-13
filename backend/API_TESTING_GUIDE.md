# Stack Overflow Clone API - Testing Guide

This guide provides comprehensive curl commands to test all the FastAPI endpoints for the Stack Overflow clone backend.

## Server Information
- **Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## Prerequisites
Make sure the FastAPI server is running:
```bash
cd stackoverflow-backend
python -m uvicorn main_simple:app --host 0.0.0.0 --port 8000 --reload
```

## Basic Endpoints

### 1. Root Endpoint
```bash
curl -s http://localhost:8000/ | python -m json.tool
```

### 2. Health Check
```bash
curl -s http://localhost:8000/health | python -m json.tool
```

## Questions API

### 3. Get All Questions (Paginated)
```bash
# Get first 15 questions (default)
curl -s http://localhost:8000/api/questions/ | python -m json.tool

# Get questions with pagination
curl -s "http://localhost:8000/api/questions/?skip=0&limit=5" | python -m json.tool

# Get questions with different pagination
curl -s "http://localhost:8000/api/questions/?skip=5&limit=10" | python -m json.tool
```

### 4. Get Specific Question
```bash
# Get question by ID (includes answers)
curl -s http://localhost:8000/api/questions/1 | python -m json.tool
curl -s http://localhost:8000/api/questions/2 | python -m json.tool
curl -s http://localhost:8000/api/questions/15 | python -m json.tool

# Test non-existent question
curl -s http://localhost:8000/api/questions/999 | python -m json.tool
```

### 5. Create Question (Mock)
```bash
# POST request to create a question
curl -X POST http://localhost:8000/api/questions/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "How to use FastAPI with MongoDB?",
    "content": "I need help connecting FastAPI to MongoDB database",
    "author_id": 1,
    "tags": ["fastapi", "mongodb", "python"]
  }' | python -m json.tool
```

## Users API

### 6. Get All Users (Paginated)
```bash
# Get first 20 users (default)
curl -s http://localhost:8000/api/users/ | python -m json.tool

# Get users with pagination
curl -s "http://localhost:8000/api/users/?skip=0&limit=5" | python -m json.tool
curl -s "http://localhost:8000/api/users/?skip=5&limit=5" | python -m json.tool
```

### 7. Get Specific User
```bash
# Get user by ID
curl -s http://localhost:8000/api/users/1 | python -m json.tool
curl -s http://localhost:8000/api/users/2 | python -m json.tool
curl -s http://localhost:8000/api/users/10 | python -m json.tool

# Test non-existent user
curl -s http://localhost:8000/api/users/999 | python -m json.tool
```

## Tags API

### 8. Get All Tags (Paginated, Sorted by Popularity)
```bash
# Get first 20 tags (default, sorted by popularity)
curl -s http://localhost:8000/api/tags/ | python -m json.tool

# Get tags with pagination
curl -s "http://localhost:8000/api/tags/?skip=0&limit=5" | python -m json.tool
curl -s "http://localhost:8000/api/tags/?skip=5&limit=10" | python -m json.tool
```

### 9. Get Specific Tag
```bash
# Get tag by name
curl -s http://localhost:8000/api/tags/javascript | python -m json.tool
curl -s http://localhost:8000/api/tags/python | python -m json.tool
curl -s http://localhost:8000/api/tags/react | python -m json.tool

# Test case-insensitive search
curl -s http://localhost:8000/api/tags/JavaScript | python -m json.tool
curl -s http://localhost:8000/api/tags/PYTHON | python -m json.tool

# Test non-existent tag
curl -s http://localhost:8000/api/tags/nonexistent | python -m json.tool
```

## Answers API

### 10. Get Answers for a Question
```bash
# Get all answers for question 1
curl -s http://localhost:8000/api/answers/question/1 | python -m json.tool

# Get answers for other questions
curl -s http://localhost:8000/api/answers/question/2 | python -m json.tool
curl -s http://localhost:8000/api/answers/question/3 | python -m json.tool

# Test question with no answers
curl -s http://localhost:8000/api/answers/question/10 | python -m json.tool
```

### 11. Get Specific Answer
```bash
# Get answer by ID
curl -s http://localhost:8000/api/answers/1 | python -m json.tool
curl -s http://localhost:8000/api/answers/2 | python -m json.tool

# Test non-existent answer
curl -s http://localhost:8000/api/answers/999 | python -m json.tool
```

### 12. Create Answer (Mock)
```bash
# POST request to create an answer
curl -X POST http://localhost:8000/api/answers/ \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Here is my answer to your question...",
    "question_id": 1,
    "author_id": 2
  }' | python -m json.tool
```

## Search API

### 13. General Search
```bash
# Search across all content types
curl -s "http://localhost:8000/api/search/?q=react" | python -m json.tool
curl -s "http://localhost:8000/api/search/?q=python" | python -m json.tool
curl -s "http://localhost:8000/api/search/?q=javascript" | python -m json.tool
curl -s "http://localhost:8000/api/search/?q=authentication" | python -m json.tool

# Search with pagination
curl -s "http://localhost:8000/api/search/?q=react&skip=0&limit=3" | python -m json.tool

# Search for partial terms
curl -s "http://localhost:8000/api/search/?q=auth" | python -m json.tool
curl -s "http://localhost:8000/api/search/?q=api" | python -m json.tool
```

## Advanced Testing

### 14. Test CORS Headers
```bash
# Check CORS headers
curl -i -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: X-Requested-With" \
  -X OPTIONS http://localhost:8000/api/questions/
```

### 15. Test Error Handling
```bash
# Test 404 errors
curl -i http://localhost:8000/api/questions/999
curl -i http://localhost:8000/api/users/999
curl -i http://localhost:8000/api/answers/999
curl -i http://localhost:8000/api/tags/nonexistent

# Test invalid endpoints
curl -i http://localhost:8000/api/invalid
curl -i http://localhost:8000/nonexistent
```

### 16. Performance Testing
```bash
# Test with larger result sets
curl -s "http://localhost:8000/api/questions/?limit=50" | python -m json.tool
curl -s "http://localhost:8000/api/users/?limit=50" | python -m json.tool
curl -s "http://localhost:8000/api/tags/?limit=50" | python -m json.tool

# Test pagination boundaries
curl -s "http://localhost:8000/api/questions/?skip=100&limit=10" | python -m json.tool
```

## Data Validation Tests

### 17. Test Data Structure
```bash
# Verify question structure includes all required fields
curl -s http://localhost:8000/api/questions/1 | jq '.id, .title, .content, .author, .votes, .views, .tags, .answers'

# Verify user structure
curl -s http://localhost:8000/api/users/1 | jq '.id, .name, .reputation, .avatar, .badges'

# Verify tag structure
curl -s http://localhost:8000/api/tags/javascript | jq '.id, .name, .description, .count'
```

### 18. Test Answer Count Calculation
```bash
# Check that questions include accurate answer counts
curl -s http://localhost:8000/api/questions/ | jq '.[] | {id: .id, title: .title, answer_count: .answer_count}'
```

### 19. Test Search Functionality
```bash
# Test different search terms
curl -s "http://localhost:8000/api/search/?q=database" | jq '.questions | length'
curl -s "http://localhost:8000/api/search/?q=framework" | jq '.questions | length'
curl -s "http://localhost:8000/api/search/?q=optimization" | jq '.questions | length'
```

## Integration Testing

### 20. Test Full Workflow
```bash
# 1. Get all questions
echo "=== Getting all questions ==="
curl -s "http://localhost:8000/api/questions/?limit=3" | jq '.[] | {id: .id, title: .title}'

# 2. Get specific question with answers
echo "=== Getting question 1 with answers ==="
curl -s http://localhost:8000/api/questions/1 | jq '{id: .id, title: .title, answer_count: (.answers | length)}'

# 3. Get question author
echo "=== Getting question author ==="
AUTHOR_ID=$(curl -s http://localhost:8000/api/questions/1 | jq '.author.id')
curl -s http://localhost:8000/api/users/$AUTHOR_ID | jq '{id: .id, name: .name, reputation: .reputation}'

# 4. Search for related content
echo "=== Searching for related content ==="
curl -s "http://localhost:8000/api/search/?q=react&limit=2" | jq '{query: .query, question_count: (.questions | length)}'
```

## Notes

- All endpoints return JSON responses
- The API includes CORS headers for frontend integration
- Mock POST endpoints return success messages without persisting data
- View count increments each time a question is accessed
- Search is case-insensitive and searches titles, content, user names, and tag names
- Pagination uses `skip` and `limit` parameters
- The server loads data from JSON files in the `data/` directory

## Expected Response Codes

- `200 OK`: Successful requests
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid request parameters

## Frontend Integration

The API is configured with CORS to allow requests from:
- `http://localhost:3000` (Next.js development server)
- `http://127.0.0.1:3000`

You can now integrate this backend with your Next.js Stack Overflow clone frontend.
