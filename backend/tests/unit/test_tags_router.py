import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.models import PaginatedResponse, Tag
from main import app

class TestTagsRouter:
    """Test tags router endpoints"""
    
    def test_get_tags_default_params(self, client, mock_data_service):
        """Test getting tags with default parameters"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "python",
                    "description": "Python programming language",
                    "count": 150
                },
                {
                    "id": 2,
                    "name": "javascript",
                    "description": "JavaScript programming language",
                    "count": 200
                }
            ],
            total=2,
            page=1,
            limit=20
        )
        mock_data_service.get_tags.return_value = mock_paginated_response
        
        response = client.get("/api/tags/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        assert data["items"][0]["name"] == "python"
        
        mock_data_service.get_tags.assert_called_with(page=1, limit=20, search=None, sort="popular")
    
    def test_get_tags_with_pagination(self, client, mock_data_service):
        """Test getting tags with pagination parameters"""
        mock_paginated_response = PaginatedResponse(
            items=[],
            total=0,
            page=2,
            limit=10
        )
        mock_data_service.get_tags.return_value = mock_paginated_response
        
        response = client.get("/api/tags/?page=2&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        
        mock_data_service.get_tags.assert_called_with(page=2, limit=10, search=None, sort="popular")
    
    def test_get_tags_with_search(self, client, mock_data_service):
        """Test getting tags with search parameter"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "python",
                    "description": "Python programming language",
                    "count": 150
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_tags.return_value = mock_paginated_response
        
        response = client.get("/api/tags/?search=python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "python"
        
        mock_data_service.get_tags.assert_called_with(page=1, limit=20, search="python", sort="popular")
    
    def test_get_tags_with_sort(self, client, mock_data_service):
        """Test getting tags with different sort options"""
        mock_paginated_response = PaginatedResponse(
            items=[],
            total=0,
            page=1,
            limit=20
        )
        mock_data_service.get_tags.return_value = mock_paginated_response
        
        # Test sort by name
        response = client.get("/api/tags/?sort=name")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_tags.assert_called_with(page=1, limit=20, search=None, sort="name")
        
        # Test sort by newest
        response = client.get("/api/tags/?sort=newest")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_tags.assert_called_with(page=1, limit=20, search=None, sort="newest")
    
    def test_get_tags_validation_errors(self, client):
        """Test validation errors for get tags endpoint"""
        # Test page too low
        response = client.get("/api/tags/?page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too high
        response = client.get("/api/tags/?limit=1000")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too low
        response = client.get("/api/tags/?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_tag_by_name_success(self, client, mock_data_service):
        """Test getting a specific tag by name"""
        mock_tag = {
            "id": 1,
            "name": "python",
            "description": "Python programming language",
            "count": 150
        }
        mock_data_service.get_tag_by_name.return_value = mock_tag
        
        response = client.get("/api/tags/python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "python"
        assert data["description"] == "Python programming language"
        assert data["count"] == 150
        
        mock_data_service.get_tag_by_name.assert_called_with("python")
    
    def test_get_tag_by_name_not_found(self, client, mock_data_service):
        """Test getting a nonexistent tag by name"""
        mock_data_service.get_tag_by_name.return_value = None
        
        response = client.get("/api/tags/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Tag not found" in data["detail"]
    
    def test_get_tag_questions_success(self, client, mock_data_service):
        """Test getting questions for a specific tag"""
        # Mock tag exists
        mock_tag = {
            "id": 1,
            "name": "python",
            "description": "Python programming language",
            "count": 150
        }
        mock_data_service.get_tag_by_name.return_value = mock_tag
        
        # Mock questions with tag
        mock_questions_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "title": "Python Question",
                    "content": "Python related content",
                    "author": {
                        "id": 1,
                        "name": "Test User",
                        "reputation": 100,
                        "avatar": "",
                        "badges": {"gold": 0, "silver": 0, "bronze": 0}
                    },
                    "tags": ["python", "programming"],
                    "votes": 8,
                    "views": 25,
                    "answer_count": 1,
                    "asked": "2024-01-15T10:30:00Z"
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_questions_by_tag.return_value = mock_questions_response
        
        response = client.get("/api/tags/python/questions")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert "python" in data["items"][0]["tags"]
        
        mock_data_service.get_tag_by_name.assert_called_with("python")
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=1, limit=20, sort="newest")
    
    def test_get_tag_questions_tag_not_found(self, client, mock_data_service):
        """Test getting questions for nonexistent tag"""
        mock_data_service.get_tag_by_name.return_value = None
        
        response = client.get("/api/tags/nonexistent/questions")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Tag not found" in data["detail"]
    
    def test_get_tag_questions_with_pagination(self, client, mock_data_service):
        """Test getting tag questions with pagination"""
        mock_tag = {
            "id": 1,
            "name": "python",
            "description": "Python programming language",
            "count": 150
        }
        mock_data_service.get_tag_by_name.return_value = mock_tag
        
        mock_questions_response = PaginatedResponse(
            items=[],
            total=0,
            page=2,
            limit=10
        )
        mock_data_service.get_questions_by_tag.return_value = mock_questions_response
        
        response = client.get("/api/tags/python/questions?page=2&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=2, limit=10, sort="newest")
    
    def test_get_tag_questions_with_sort(self, client, mock_data_service):
        """Test getting tag questions with different sort options"""
        mock_tag = {
            "id": 1,
            "name": "python",
            "description": "Python programming language",
            "count": 150
        }
        mock_data_service.get_tag_by_name.return_value = mock_tag
        
        mock_questions_response = PaginatedResponse(
            items=[],
            total=0,
            page=1,
            limit=20
        )
        mock_data_service.get_questions_by_tag.return_value = mock_questions_response
        
        # Test sort by votes
        response = client.get("/api/tags/python/questions?sort=votes")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=1, limit=20, sort="votes")
        
        # Test sort by activity
        response = client.get("/api/tags/python/questions?sort=activity")
        assert response.status_code == status.HTTP_200_OK
        mock_data_service.get_questions_by_tag.assert_called_with("python", page=1, limit=20, sort="activity")
    
    def test_get_popular_tags_success(self, client, mock_data_service):
        """Test getting popular tags"""
        mock_popular_tags = [
            {
                "id": 1,
                "name": "javascript",
                "description": "JavaScript programming language",
                "count": 200
            },
            {
                "id": 2,
                "name": "python",
                "description": "Python programming language",
                "count": 150
            }
        ]
        mock_data_service.get_popular_tags.return_value = mock_popular_tags
        
        response = client.get("/api/tags/stats/popular")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tags" in data
        assert len(data["tags"]) == 2
        assert data["tags"][0]["name"] == "javascript"
        
        mock_data_service.get_popular_tags.assert_called_with(limit=10)
    
    def test_get_popular_tags_with_limit(self, client, mock_data_service):
        """Test getting popular tags with custom limit"""
        mock_data_service.get_popular_tags.return_value = []
        
        response = client.get("/api/tags/stats/popular?limit=5")
        assert response.status_code == status.HTTP_200_OK
        
        mock_data_service.get_popular_tags.assert_called_with(limit=5)
    
    def test_get_popular_tags_validation_errors(self, client):
        """Test validation errors for popular tags endpoint"""
        # Test limit too low
        response = client.get("/api/tags/stats/popular?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too high
        response = client.get("/api/tags/stats/popular?limit=100")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_trending_tags_success(self, client, mock_data_service):
        """Test getting trending tags"""
        mock_trending_tags = [
            {
                "id": 3,
                "name": "fastapi",
                "description": "FastAPI web framework",
                "count": 45
            },
            {
                "id": 4,
                "name": "react",
                "description": "React JavaScript library",
                "count": 120
            }
        ]
        mock_data_service.get_trending_tags.return_value = mock_trending_tags
        
        response = client.get("/api/tags/stats/trending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tags" in data
        assert len(data["tags"]) == 2
        assert data["tags"][0]["name"] == "fastapi"
        
        mock_data_service.get_trending_tags.assert_called_with(limit=10)
    
    def test_get_trending_tags_with_limit(self, client, mock_data_service):
        """Test getting trending tags with custom limit"""
        mock_data_service.get_trending_tags.return_value = []
        
        response = client.get("/api/tags/stats/trending?limit=15")
        assert response.status_code == status.HTTP_200_OK
        
        mock_data_service.get_trending_tags.assert_called_with(limit=15)
    
    def test_get_trending_tags_validation_errors(self, client):
        """Test validation errors for trending tags endpoint"""
        # Test limit too low
        response = client.get("/api/tags/stats/trending?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test limit too high
        response = client.get("/api/tags/stats/trending?limit=100")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_tags_router_error_handling(self, client, mock_data_service):
        """Test error handling in tags router"""
        # Store original return value
        original_return_value = mock_data_service.get_tags.return_value
        
        # Test service error
        mock_data_service.get_tags.side_effect = Exception("Database error")
        
        # In test environment, the exception propagates instead of returning 500
        try:
            response = client.get("/api/tags/")
            # If no exception, check for 500 status
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            # Exception propagated as expected in test environment
            assert str(e) == "Database error"
        
        # Reset the mock properly
        mock_data_service.get_tags.side_effect = None
        mock_data_service.get_tags.return_value = original_return_value
    
    def test_tags_response_model_validation(self, client, mock_data_service):
        """Test that response data matches the expected model structure"""
        mock_paginated_response = PaginatedResponse(
            items=[
                {
                    "id": 1,
                    "name": "python",
                    "description": "Python programming language",
                    "count": 150
                }
            ],
            total=1,
            page=1,
            limit=20
        )
        mock_data_service.get_tags.return_value = mock_paginated_response
        
        response = client.get("/api/tags/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure matches PaginatedResponse[Tag] model
        required_fields = ["items", "total", "page", "limit"]
        for field in required_fields:
            assert field in data
        
        # Verify tag structure
        if data["items"]:
            tag = data["items"][0]
            tag_fields = ["id", "name", "description", "count"]
            for field in tag_fields:
                assert field in tag
