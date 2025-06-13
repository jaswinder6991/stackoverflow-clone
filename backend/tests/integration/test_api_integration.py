import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
import json
import tempfile
import os

class TestAPIIntegration:
    """Integration tests for the complete API"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for integration tests"""
        return TestClient(app)
    
    def test_api_health_check(self, client):
        """Test basic API health check"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_api_root_endpoint(self, client):
        """Test API root endpoint"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Stack Overflow Clone API" in data["message"]
        assert "version" in data
        assert "docs" in data
    
    def test_questions_list_integration(self, client):
        """Test questions listing endpoint integration"""
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        
        # If there are questions, verify structure
        if data:
            question = data[0]
            required_fields = ["id", "title", "content", "author", "tags", "votes", "views", "answer_count", "asked"]
            for field in required_fields:
                assert field in question
    
    def test_questions_pagination_integration(self, client):
        """Test questions pagination works correctly"""
        # Test different page sizes
        response1 = client.get("/api/questions/?limit=1")
        assert response1.status_code == status.HTTP_200_OK
        data1 = response1.json()
        
        response2 = client.get("/api/questions/?limit=5")
        assert response2.status_code == status.HTTP_200_OK
        data2 = response2.json()
        
        # Should handle different limits correctly
        assert len(data1) <= 1
        assert len(data2) <= 5
    
    def test_question_detail_integration(self, client):
        """Test question detail endpoint integration"""
        # First get a list of questions to get a valid ID
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        questions = response.json()
        
        if questions:
            question_id = questions[0]["id"]
            detail_response = client.get(f"/api/questions/{question_id}")
            assert detail_response.status_code == status.HTTP_200_OK
            
            detail_data = detail_response.json()
            assert detail_data["id"] == question_id
            assert "answers" in detail_data
    
    def test_users_list_integration(self, client):
        """Test users listing endpoint integration"""
        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return paginated response
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        
        # If there are users, verify structure
        if data["items"]:
            user = data["items"][0]
            required_fields = ["id", "name", "reputation", "avatar", "badges"]
            for field in required_fields:
                assert field in user
    
    def test_user_detail_integration(self, client):
        """Test user detail endpoint integration"""
        # First get a list of users to get a valid ID
        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        users_data = response.json()
        
        if users_data["items"]:
            user_id = users_data["items"][0]["id"]
            detail_response = client.get(f"/api/users/{user_id}")
            assert detail_response.status_code == status.HTTP_200_OK
            
            detail_data = detail_response.json()
            assert detail_data["id"] == user_id
    
    def test_tags_list_integration(self, client):
        """Test tags listing endpoint integration"""
        response = client.get("/api/tags/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return paginated response
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        
        # If there are tags, verify structure
        if data["items"]:
            tag = data["items"][0]
            required_fields = ["id", "name", "description", "count"]
            for field in required_fields:
                assert field in tag
    
    def test_search_integration(self, client):
        """Test search functionality integration"""
        response = client.get("/api/search/?q=python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return search response structure
        assert "query" in data
        assert "total_results" in data
        assert data["query"] == "python"
    
    def test_search_questions_integration(self, client):
        """Test search questions endpoint integration"""
        response = client.get("/api/search/questions?q=test")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should return paginated response
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
    
    def test_cors_headers_integration(self, client):
        """Test CORS headers are properly set"""
        response = client.options("/api/questions/")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]
        
        # Test with Origin header
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/api/questions/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
    
    def test_error_handling_integration(self, client):
        """Test error handling across the API"""
        # Test 404 errors
        response = client.get("/api/questions/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        response = client.get("/api/users/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        response = client.get("/api/tags/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Test invalid endpoints
        response = client.get("/api/invalid")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_parameter_validation_integration(self, client):
        """Test parameter validation across endpoints"""
        # Test invalid pagination parameters
        response = client.get("/api/questions/?skip=-1")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.get("/api/questions/?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.get("/api/users/?page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.get("/api/tags/?limit=1000")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_api_consistency_integration(self, client):
        """Test API consistency across endpoints"""
        # Test that all paginated endpoints return consistent structure
        endpoints = [
            "/api/users/",
            "/api/tags/",
            "/api/search/questions?q=test",
            "/api/search/users?q=test",
            "/api/search/tags?q=test"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
                # Check for consistent pagination structure
                if isinstance(data, dict) and "items" in data:
                    pagination_fields = ["items", "total", "page", "limit"]
                    for field in pagination_fields:
                        assert field in data, f"Missing {field} in {endpoint}"
    
    def test_data_relationships_integration(self, client):
        """Test data relationships work correctly"""
        # Get a question with answers
        response = client.get("/api/questions/")
        assert response.status_code == status.HTTP_200_OK
        questions = response.json()
        
        if questions:
            question_id = questions[0]["id"]
            
            # Get question detail
            detail_response = client.get(f"/api/questions/{question_id}")
            assert detail_response.status_code == status.HTTP_200_OK
            question_detail = detail_response.json()
            
            # Get answers for the question
            answers_response = client.get(f"/api/answers/question/{question_id}")
            assert answers_response.status_code == status.HTTP_200_OK
            
            # Verify consistency between question detail and answers endpoint
            if "answers" in question_detail:
                answers_from_question = question_detail["answers"]
                answers_from_endpoint = answers_response.json()
                
                # Should have consistent answer data
                if isinstance(answers_from_endpoint, list):
                    assert len(answers_from_question) == len(answers_from_endpoint)
    
    def test_search_functionality_integration(self, client):
        """Test complete search functionality"""
        # Test search across different types
        search_types = ["questions", "users", "tags"]
        
        for search_type in search_types:
            response = client.get(f"/api/search/{search_type}?q=test")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            
            # Should return paginated response
            assert "items" in data
            assert "total" in data
    
    def test_tag_filtering_integration(self, client):
        """Test tag-based filtering works correctly"""
        # Get available tags
        tags_response = client.get("/api/tags/")
        assert tags_response.status_code == status.HTTP_200_OK
        tags_data = tags_response.json()
        
        if tags_data["items"]:
            tag_name = tags_data["items"][0]["name"]
            
            # Test questions filtered by tag using the actual available endpoint
            tagged_response = client.get(f"/api/questions/?tag={tag_name}")
            assert tagged_response.status_code == status.HTTP_200_OK
            tagged_questions = tagged_response.json()
            
            # All returned questions should have the tag
            if tagged_questions:
                for question in tagged_questions:
                    assert tag_name in question["tags"]
    
    def test_performance_integration(self, client):
        """Test API performance with various loads"""
        import time
        
        # Test response times for different endpoints
        endpoints = [
            "/api/questions/",
            "/api/users/",
            "/api/tags/",
            "/api/search/?q=test"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == status.HTTP_200_OK
            response_time = end_time - start_time
            # API should respond within reasonable time (5 seconds for integration tests)
            assert response_time < 5.0, f"Endpoint {endpoint} took {response_time:.2f}s"
    
    def test_api_documentation_integration(self, client):
        """Test API documentation endpoints are accessible"""
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        
        # Test Swagger UI
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
        
        # Test ReDoc
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
