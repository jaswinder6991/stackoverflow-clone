import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.routers.questions import router
from app.models import PaginatedResponse, QuestionSummary, Question, User, UserBadges
from main import app

class TestQuestionsRouter:
    """Test questions router endpoints"""
    
    def test_get_questions_default_params(self, client, mock_data_service):
        """Test getting questions with default parameters"""
        # Mock the data service response
        mock_data_service.get_questions.return_value = [
            {
                "id": 1,
                "title": "Test Question",
                "content": "Test content",
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["python"],
                "votes": 5,
                "views": 10,
                "answer_count": 2,
                "asked": "2024-01-15T10:30:00Z"
            }
        ]
        
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["title"] == "Test Question"
        assert data[0]["answer_count"] == 2
    
    def test_get_questions_with_pagination(self, client, mock_data_service):
        """Test getting questions with pagination parameters"""
        mock_data_service.get_questions.return_value = []
        
        response = client.get("/api/questions/?skip=10&limit=5")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the service was called with correct parameters
        mock_data_service.get_questions.assert_called_with(skip=10, limit=5, sort="newest")
    
    def test_get_questions_with_sort(self, client, mock_data_service):
        """Test getting questions with different sort options"""
        mock_data_service.get_questions.return_value = []
        
        response = client.get("/api/questions/?sort=votes")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_questions.assert_called_with(skip=0, limit=15, sort="votes")
        
        response = client.get("/api/questions/?sort=active")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_questions.assert_called_with(skip=0, limit=15, sort="active")
    
    def test_get_questions_with_tag_filter(self, client, mock_data_service):
        """Test getting questions filtered by tag"""
        mock_paginated_response = PaginatedResponse(
            items=[{
                "id": 1,
                "title": "Python Question",
                "content": "Python content",
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["python"],
                "votes": 5,
                "views": 10,
                "answer_count": 1,
                "asked": "2024-01-15T10:30:00Z"
            }],
            total=1,
            page=1,
            limit=15
        )
        mock_data_service.get_questions_by_tag.return_value = mock_paginated_response
        
        response = client.get("/api/questions/?tag=python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "python" in data[0]["tags"]
        
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=1, limit=15)
    
    def test_get_questions_with_user_filter(self, client, mock_data_service):
        """Test getting questions filtered by user"""
        mock_paginated_response = PaginatedResponse(
            items=[{
                "id": 1,
                "title": "User Question",
                "content": "User content",
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["test"],
                "votes": 5,
                "views": 10,
                "answer_count": 0,
                "asked": "2024-01-15T10:30:00Z"
            }],
            total=1,
            page=1,
            limit=15
        )
        mock_data_service.get_questions_by_user.return_value = mock_paginated_response
        
        response = client.get("/api/questions/?user_id=1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["author"]["id"] == 1
        
        mock_data_service.get_questions_by_user.assert_called_with(1, page=1, limit=15)
    
    def test_get_questions_validation_errors(self, client):
        """Test validation errors for get questions endpoint"""
        # Test negative skip
        response = client.get("/api/questions/?skip=-1")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too high
        response = client.get("/api/questions/?limit=1000")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too low
        response = client.get("/api/questions/?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_question_by_id_success(self, client, mock_data_service):
        """Test getting a specific question by ID"""
        # Use global mock data instead of overriding
        response = client.get("/api/questions/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        # Use actual title from global mock data
        assert data["title"] == "How to use Python with FastAPI?"
        assert "answers" in data
        
        mock_data_service.get_question_by_id.assert_called_with(1)
    
    def test_get_question_by_id_not_found(self, client, mock_data_service):
        """Test getting a nonexistent question by ID"""
        mock_data_service.get_question_by_id.return_value = None
        
        response = client.get("/api/questions/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Question not found" in data["detail"]
    
    def test_search_questions_success(self, client, mock_data_service):
        """Test searching questions"""
        # Use global mock data that returns tuple format
        response = client.get("/api/questions/search?q=python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Should return a list of questions
        assert isinstance(data, list)
        # Verify the service was called with correct parameters
        mock_data_service.search_questions.assert_called_with(
            query="python", tags=[], skip=0, limit=15, sort="relevance"
        )
    
    def test_search_questions_with_tags(self, client, mock_data_service):
        """Test searching questions with tag filters"""
        # Override to return empty tuple for this specific test
        mock_data_service.search_questions.return_value = ([], 0)
        
        response = client.get("/api/questions/search?q=test&tags=python&tags=fastapi")
        assert response.status_code == status.HTTP_200_OK
        
        # Note: The actual implementation may handle multiple tags differently
        # This test ensures the endpoint accepts the parameter structure
    
    def test_search_questions_missing_query(self, client):
        """Test searching questions without query parameter"""
        response = client.get("/api/questions/search")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_search_questions_empty_results(self, client, mock_data_service):
        """Test searching questions with no results"""
        # Override to return empty tuple for this specific test
        mock_data_service.search_questions.return_value = ([], 0)
        
        response = client.get("/api/questions/search?q=nonexistent")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
    
    def test_get_questions_tagged_success(self, client, mock_data_service):
        """Test getting questions by tag"""
        mock_paginated_response = PaginatedResponse(
            items=[{
                "id": 1,
                "title": "Python Question",
                "content": "Python related content",
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["python", "programming"],
                "votes": 8,
                "views": 25,
                "answer_count": 1,
                "asked": "2024-01-15T10:30:00Z"
            }],
            total=1,
            page=1,
            limit=15
        )
        mock_data_service.get_questions_by_tag.return_value = mock_paginated_response
        
        response = client.get("/api/questions/tagged/python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert "python" in data[0]["tags"]
        
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=1, limit=15)
    
    def test_get_questions_tagged_empty(self, client, mock_data_service):
        """Test getting questions by tag with no results"""
        mock_data_service.get_questions_by_tag.return_value = PaginatedResponse(
            items=[], total=0, page=1, limit=15
        )
        
        response = client.get("/api/questions/tagged/nonexistent")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
    
    def test_content_truncation(self, client, mock_data_service):
        """Test that question content is truncated in list view"""
        long_content = "A" * 300  # Content longer than 200 characters
        mock_data_service.get_questions.return_value = [
            {
                "id": 1,
                "title": "Test Question",
                "content": long_content,
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["test"],
                "votes": 1,
                "views": 1,
                "answer_count": 0,
                "asked": "2024-01-15T10:30:00Z"
            }
        ]
        
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data[0]["content"]) <= 203  # 200 chars + "..."
        assert data[0]["content"].endswith("...")
    
    def test_questions_router_error_handling(self, client, mock_data_service):
        """Test error handling in questions router"""
        # Store original return value
        original_return_value = mock_data_service.get_questions.return_value
        
        # Test service error
        mock_data_service.get_questions.side_effect = Exception("Database error")
        
        # In test environment, the exception propagates instead of returning 500
        try:
            response = client.get("/api/questions/")
            # If no exception, check for 500 status
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            # Exception propagated as expected in test environment
            assert str(e) == "Database error"
        
        # Reset the mock properly
        mock_data_service.get_questions.side_effect = None
        mock_data_service.get_questions.return_value = original_return_value
    
    def test_questions_response_model_validation(self, client, mock_data_service):
        """Test that response data matches the expected model structure"""
        mock_data_service.get_questions.return_value = [
            {
                "id": 1,
                "title": "Test Question",
                "content": "Test content",
                "author": {"id": 1, "name": "Test User", "reputation": 100, "avatar": "", "badges": {"gold": 0, "silver": 0, "bronze": 0}},
                "tags": ["python"],
                "votes": 5,
                "views": 10,
                "answer_count": 2,
                "asked": "2024-01-15T10:30:00Z"
            }
        ]
        
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure matches QuestionSummary model
        question = data[0]
        required_fields = ["id", "title", "content", "author", "tags", "votes", "views", "answer_count", "asked"]
        for field in required_fields:
            assert field in question
        
        # Verify author structure
        author = question["author"]
        author_fields = ["id", "name", "reputation", "avatar", "badges"]
        for field in author_fields:
            assert field in author
