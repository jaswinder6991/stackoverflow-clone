import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.models import PaginatedResponse, User, UserBadges
from main import app

class TestUsersRouter:
    """Test users router endpoints"""
    
    def test_get_users_default_params(self, client, mock_data_service):
        """Test getting users with default parameters"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "John Doe",
                    "reputation": 1500,
                    "avatar": "https://example.com/avatar1.jpg",
                    "location": "New York",
                    "badges": {"gold": 2, "silver": 5, "bronze": 10}
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_users.return_value = mock_paginated_response
        
        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "John Doe"
        
        mock_data_service.get_users.assert_called_with(page=1, limit=20, search=None)
    
    def test_get_users_with_pagination(self, client, mock_data_service):
        """Test getting users with pagination parameters"""
        mock_paginated_response = PaginatedResponse(
            items=[],
            total=0,
            page=2,
            limit=10
        )
        mock_data_service.get_users.return_value = mock_paginated_response
        
        response = client.get("/api/users/?page=2&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        
        mock_data_service.get_users.assert_called_with(page=2, limit=10, search=None)
    
    def test_get_users_with_search(self, client, mock_data_service):
        """Test getting users with search parameter"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "John Doe",
                    "reputation": 1500,
                    "avatar": "https://example.com/avatar1.jpg",
                    "location": "New York",
                    "badges": {"gold": 2, "silver": 5, "bronze": 10}
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_users.return_value = mock_paginated_response
        
        response = client.get("/api/users/?search=john")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert "John" in data["items"][0]["name"]
        
        mock_data_service.get_users.assert_called_with(page=1, limit=20, search="john")
    
    def test_get_users_validation_errors(self, client):
        """Test validation errors for get users endpoint"""
        # Test page too low
        response = client.get("/api/users/?page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too high
        response = client.get("/api/users/?limit=1000")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too low
        response = client.get("/api/users/?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_user_by_id_success(self, client, mock_data_service):
        """Test getting a specific user by ID"""
        mock_user = {
            "id": 1,
            "name": "John Doe",
            "reputation": 1500,
            "avatar": "https://example.com/avatar1.jpg",
            "location": "New York",
            "badges": {"gold": 2, "silver": 5, "bronze": 10}
        }
        mock_data_service.get_user_by_id.return_value = mock_user
        
        response = client.get("/api/users/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["reputation"] == 1500
        
        mock_data_service.get_user_by_id.assert_called_with(1)
    
    def test_get_user_by_id_not_found(self, client, mock_data_service):
        """Test getting a nonexistent user by ID"""
        mock_data_service.get_user_by_id.return_value = None
        
        response = client.get("/api/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "User not found" in data["detail"]
    
    def test_get_user_questions_success(self, client, mock_data_service):
        """Test getting questions by a specific user"""
        # Mock user exists
        mock_user = {
            "id": 1,
            "name": "John Doe",
            "reputation": 1500,
            "avatar": "https://example.com/avatar1.jpg",
            "location": "New York",
            "badges": {"gold": 2, "silver": 5, "bronze": 10}
        }
        mock_data_service.get_user_by_id.return_value = mock_user
        
        # Mock user questions
        mock_questions_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "title": "User's Question",
                    "content": "Question content",
                    "author": mock_user,
                    "tags": ["python"],
                    "votes": 5,
                    "views": 10,
                    "answer_count": 2,
                    "asked": "2024-01-15T10:30:00Z"
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_questions_by_user.return_value = mock_questions_response
        
        response = client.get("/api/users/1/questions")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "User's Question"
        
        mock_data_service.get_user_by_id.assert_called_with(1)
        mock_data_service.get_questions_by_user.assert_called_with(1, page=1, limit=20)
    
    def test_get_user_questions_user_not_found(self, client, mock_data_service):
        """Test getting questions for nonexistent user"""
        mock_data_service.get_user_by_id.return_value = None
        
        response = client.get("/api/users/999/questions")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "User not found" in data["detail"]
    
    def test_get_user_questions_with_pagination(self, client, mock_data_service):
        """Test getting user questions with pagination"""
        mock_user = {
            "id": 1,
            "name": "John Doe",
            "reputation": 1500,
            "avatar": "https://example.com/avatar1.jpg",
            "location": "New York",
            "badges": {"gold": 2, "silver": 5, "bronze": 10}
        }
        mock_data_service.get_user_by_id.return_value = mock_user
        
        mock_questions_response = PaginatedResponse(
            items=[],
            total=0,
            page=2,
            limit=10
        )
        mock_data_service.get_questions_by_user.return_value = mock_questions_response
        
        response = client.get("/api/users/1/questions?page=2&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        
        mock_data_service.get_questions_by_user.assert_called_with(1, page=2, limit=10)
    
    def test_get_user_answers_success(self, client, mock_data_service):
        """Test getting answers by a specific user"""
        # Mock user exists
        mock_user = {
            "id": 1,
            "name": "John Doe",
            "reputation": 1500,
            "avatar": "https://example.com/avatar1.jpg",
            "location": "New York",
            "badges": {"gold": 2, "silver": 5, "bronze": 10}
        }
        mock_data_service.get_user_by_id.return_value = mock_user
        
        # Mock user answers
        mock_answers_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "content": "User's answer",
                    "author": mock_user,
                    "question_id": 1,
                    "votes": 3,
                    "is_accepted": True,
                    "answered": "2024-01-15T12:00:00Z"
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_answers_by_user.return_value = mock_answers_response
        
        response = client.get("/api/users/1/answers")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["content"] == "User's answer"
        
        mock_data_service.get_user_by_id.assert_called_with(1)
        mock_data_service.get_answers_by_user.assert_called_with(1, page=1, limit=20)
    
    def test_get_user_answers_user_not_found(self, client, mock_data_service):
        """Test getting answers for nonexistent user"""
        mock_data_service.get_user_by_id.return_value = None
        
        response = client.get("/api/users/999/answers")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "User not found" in data["detail"]
    
    def test_get_user_answers_with_pagination(self, client, mock_data_service):
        """Test getting user answers with pagination"""
        mock_user = {
            "id": 1,
            "name": "John Doe",
            "reputation": 1500,
            "avatar": "https://example.com/avatar1.jpg",
            "location": "New York",
            "badges": {"gold": 2, "silver": 5, "bronze": 10}
        }
        mock_data_service.get_user_by_id.return_value = mock_user
        
        mock_answers_response = PaginatedResponse(
            items=[],
            total=0,
            page=3,
            limit=5
        )
        mock_data_service.get_answers_by_user.return_value = mock_answers_response
        
        response = client.get("/api/users/1/answers?page=3&limit=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 3
        assert data["limit"] == 5
        
        mock_data_service.get_answers_by_user.assert_called_with(1, page=3, limit=5)
    
    def test_users_router_error_handling(self, client, mock_data_service):
        """Test error handling in users router"""
        # Store original return value
        original_return_value = mock_data_service.get_users.return_value
        
        # Test service error
        mock_data_service.get_users.side_effect = Exception("Database error")
        
        # In test environment, the exception propagates instead of returning 500
        try:
            response = client.get("/api/users/")
            # If no exception, check for 500 status
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            # Exception propagated as expected in test environment
            assert str(e) == "Database error"
        
        # Reset the mock properly
        mock_data_service.get_users.side_effect = None
        mock_data_service.get_users.return_value = original_return_value
    
    def test_users_response_model_validation(self, client, mock_data_service):
        """Test that response data matches the expected model structure"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "John Doe",
                    "reputation": 1500,
                    "avatar": "https://example.com/avatar1.jpg",
                    "location": "New York",
                    "badges": {"gold": 2, "silver": 5, "bronze": 10}
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_users.return_value = mock_paginated_response
        
        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure matches PaginatedResponse[User] model
        required_fields = ["items", "total", "page", "limit"]
        for field in required_fields:
            assert field in data
        
        # Verify user structure
        if data["items"]:
            user = data["items"][0]
            user_fields = ["id", "name", "reputation", "avatar", "badges"]
            for field in user_fields:
                assert field in user
            
            # Verify badges structure
            badges = user["badges"]
            badge_fields = ["gold", "silver", "bronze"]
            for field in badge_fields:
                assert field in badges
