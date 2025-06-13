import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.models import Answer, AnswerCreate, AnswerUpdate, MessageResponse, PaginatedResponse
from main import app

class TestAnswersRouter:
    """Test answers router endpoints"""
    
    def test_get_answers_by_question_success(self, client, mock_data_service):
        """Test getting answers for a question"""
        # Don't override the mock - use the global conftest mock data
        response = client.get("/api/answers/question/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure
        assert isinstance(data, list)
        assert len(data) == 2  # Global mock has 2 answers
        
        # Verify answer structure
        answer = data[0]
        assert "id" in answer
        assert "content" in answer
        assert "author" in answer
        assert "votes" in answer
        assert "is_accepted" in answer
        assert "answered" in answer
    
    def test_get_answers_by_question_no_answers(self, client, mock_data_service):
        """Test getting answers for a question with no answers"""
        # Override mock to return empty list
        mock_data_service.get_answers_by_question.return_value = []
        
        response = client.get("/api/answers/question/999")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []
    
    def test_get_answers_by_question_with_pagination(self, client, mock_data_service):
        """Test getting answers with pagination"""
        # Don't override the mock - use the global conftest mock data
        response = client.get("/api/answers/question/1?skip=0&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_answer_by_id_success(self, client, mock_data_service):
        """Test getting a specific answer by ID"""
        # Don't override the mock - use the global conftest mock data
        response = client.get("/api/answers/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify answer structure
        assert data["id"] == 1
        assert "content" in data
        assert "author" in data
        assert "votes" in data
        assert "is_accepted" in data
        assert "answered" in data
    
    def test_get_answer_by_id_not_found(self, client, mock_data_service):
        """Test getting non-existent answer"""
        # Override mock to return None
        mock_data_service.get_answer_by_id.return_value = None
        
        response = client.get("/api/answers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Answer not found" in response.json()["detail"]
    
    def test_create_answer_success(self, client, mock_data_service):
        """Test creating a new answer"""
        answer_data = {
            "content": "This is a test answer",
            "question_id": 1,
            "author_id": 1,
            "answered": "2024-01-15T10:30:00Z"
        }
        
        response = client.post("/api/answers/", json=answer_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "would be created for question" in data["message"]
        assert data["success"] is True
    
    def test_create_answer_question_not_found(self, client, mock_data_service):
        """Test creating answer for non-existent question"""
        # Override mock to return None for question
        mock_data_service.get_question_by_id.return_value = None
        
        answer_data = {
            "content": "This is a test answer",
            "question_id": 999,
            "author_id": 1,
            "answered": "2024-01-15T10:30:00Z"
        }
        
        response = client.post("/api/answers/", json=answer_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Question not found" in response.json()["detail"]
    
    def test_create_answer_user_not_found(self, client, mock_data_service):
        """Test creating answer for non-existent user"""
        # Override mock to return None for user
        mock_data_service.get_user_by_id.return_value = None
        
        answer_data = {
            "content": "This is a test answer",
            "question_id": 1,
            "author_id": 999,
            "answered": "2024-01-15T10:30:00Z"
        }
        
        response = client.post("/api/answers/", json=answer_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]
    
    def test_create_answer_validation_errors(self, client):
        """Test validation errors for answer creation"""
        # Test missing required fields
        response = client.post("/api/answers/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test invalid data types
        response = client.post("/api/answers/", json={
            "content": "",  # Empty content
            "question_id": "invalid",
            "author_id": "invalid"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_answer_success(self, client, mock_data_service):
        """Test updating an existing answer"""
        update_data = {
            "content": "Updated answer content"
        }
        
        response = client.put("/api/answers/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "would be updated" in data["message"]
        assert data["success"] is True
    
    def test_update_answer_not_found(self, client, mock_data_service):
        """Test updating non-existent answer"""
        # Override mock to return None
        mock_data_service.get_answer_by_id.return_value = None
        
        update_data = {
            "content": "Updated answer content"
        }
        
        response = client.put("/api/answers/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Answer not found" in response.json()["detail"]
    
    def test_delete_answer_success(self, client, mock_data_service):
        """Test deleting an existing answer"""
        response = client.delete("/api/answers/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "would be deleted" in data["message"]
        assert data["success"] is True
    
    def test_delete_answer_not_found(self, client, mock_data_service):
        """Test deleting non-existent answer"""
        # Override mock to return None
        mock_data_service.get_answer_by_id.return_value = None
        
        response = client.delete("/api/answers/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Answer not found" in response.json()["detail"]
    
    def test_vote_answer_success(self, client, mock_data_service):
        """Test voting on an answer"""
        response = client.post("/api/answers/1/vote?vote_type=up")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Vote 'up' registered" in data["message"]
        assert data["success"] is True
        
        response = client.post("/api/answers/1/vote?vote_type=down")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Vote 'down' registered" in data["message"]
        assert data["success"] is True
    
    def test_vote_answer_not_found(self, client, mock_data_service):
        """Test voting on non-existent answer"""
        # Override mock to return None
        mock_data_service.get_answer_by_id.return_value = None
        
        response = client.post("/api/answers/999/vote?vote_type=up")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Answer not found" in response.json()["detail"]
    
    def test_accept_answer_success(self, client, mock_data_service):
        """Test accepting an answer"""
        response = client.post("/api/answers/1/accept")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "would be marked as accepted" in data["message"]
        assert data["success"] is True
    
    def test_answers_router_error_handling(self, client, mock_data_service):
        """Test router error handling when data service fails"""
        # Store original return value
        original_return_value = mock_data_service.get_answers_by_question.return_value
        
        # Test service error by making get_answers_by_question raise an exception
        mock_data_service.get_answers_by_question.side_effect = Exception("Database error")
        
        # In test environment, the exception propagates instead of returning 500
        try:
            response = client.get("/api/answers/question/1")
            # If no exception, check for 500 status
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            # Exception propagated as expected in test environment
            assert str(e) == "Database error"
        
        # Reset the mock properly
        mock_data_service.get_answers_by_question.side_effect = None
        mock_data_service.get_answers_by_question.return_value = original_return_value
    
    def test_answers_response_model_validation(self, client, mock_data_service):
        """Test that response data matches the expected model structure"""
        # Don't override the mock - use the global conftest mock data
        response = client.get("/api/answers/question/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verify response structure
        assert isinstance(data, list)
        if data:
            answer = data[0]
            required_fields = ["id", "content", "author", "votes", "is_accepted", "answered"]
            for field in required_fields:
                assert field in answer
                
            # Verify author structure
            author = answer["author"]
            author_fields = ["id", "name", "reputation", "avatar", "badges"]
            for field in author_fields:
                assert field in author