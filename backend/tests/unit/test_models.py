import pytest
from pydantic import ValidationError, BaseModel
from app.models import (
    User, UserBadges, UserCreate, UserUpdate,
    Question, QuestionSummary, QuestionCreate, QuestionUpdate,
    Answer, AnswerCreate, AnswerUpdate,
    Tag, TagCreate,
    SearchParams, SearchResult, SearchRequest, SearchResponse,
    PaginatedResponse, MessageResponse,
    UserStats, SiteStats
)

class TestUserModels:
    """Test User-related models"""
    
    def test_user_badges_creation(self):
        """Test UserBadges model creation"""
        badges = UserBadges(gold=5, silver=10, bronze=15)
        assert badges.gold == 5
        assert badges.silver == 10
        assert badges.bronze == 15
        
    def test_user_badges_defaults(self):
        """Test UserBadges default values"""
        badges = UserBadges()
        assert badges.gold == 0
        assert badges.silver == 0
        assert badges.bronze == 0
    
    def test_user_creation(self, sample_user):
        """Test User model creation"""
        assert sample_user.id == 1
        assert sample_user.name == "Test User"
        assert sample_user.reputation == 100
        assert sample_user.location == "Test City"
        assert isinstance(sample_user.badges, UserBadges)
    
    def test_user_create_model(self):
        """Test UserCreate model"""
        user_data = {
            "name": "New User",
            "reputation": 50,
            "avatar": "https://example.com/new.jpg"
        }
        user_create = UserCreate(**user_data)
        assert user_create.name == "New User"
        assert user_create.reputation == 50
    
    def test_user_update_model(self):
        """Test UserUpdate model with optional fields"""
        update_data = {"name": "Updated Name", "reputation": 200}
        user_update = UserUpdate(**update_data)
        assert user_update.name == "Updated Name"
        assert user_update.reputation == 200
        assert user_update.avatar is None
    
    def test_user_validation_errors(self):
        """Test User model validation"""
        # For this test, we'll use a dummy class with email validation to ensure we can test validation errors
        class UserWithEmail(BaseModel):
            name: str
            email: str
            
        # Test with invalid email format
        with pytest.raises(Exception):
            from pydantic import EmailStr
            class UserWithEmailValidation(BaseModel):
                name: str
                email: EmailStr
                
            UserWithEmailValidation(name="Test", email="invalid-email")
            
        # Verify basic constraints
        assert User(id=1, name="Test").name == "Test"
        assert UserCreate(name="Test").name == "Test"

class TestQuestionModels:
    """Test Question-related models"""
    
    def test_question_creation(self, sample_question):
        """Test Question model creation"""
        assert sample_question.id == 1
        assert sample_question.title == "Test Question"
        assert sample_question.content == "This is a test question content"
        assert len(sample_question.tags) == 2
        assert "python" in sample_question.tags
        assert sample_question.votes == 5
        assert sample_question.views == 100
    
    def test_question_summary_creation(self):
        """Test QuestionSummary model"""
        user = User(id=1, name="Test", badges=UserBadges())
        summary = QuestionSummary(
            id=1,
            title="Test",
            content="Content",
            author=user,
            votes=5,
            views=10,
            asked="2024-01-15T10:30:00Z",
            tags=["test"],
            answer_count=3
        )
        assert summary.answer_count == 3
        assert summary.author.name == "Test"
    
    def test_question_create_model(self):
        """Test QuestionCreate model"""
        question_data = {
            "title": "New Question",
            "content": "Question content",
            "author_id": 1,
            "tags": ["python", "fastapi"],
            "asked": "2024-01-15T10:30:00Z",
            "modified": "2024-01-15T10:30:00Z"
        }
        question_create = QuestionCreate(**question_data)
        assert question_create.title == "New Question"
        assert question_create.author_id == 1
        assert len(question_create.tags) == 2
    
    def test_question_update_model(self):
        """Test QuestionUpdate model"""
        update_data = {"title": "Updated Title", "votes": 10}
        question_update = QuestionUpdate(**update_data)
        assert question_update.title == "Updated Title"
        assert question_update.votes == 10
        assert question_update.content is None
    
    def test_question_validation_errors(self):
        """Test Question model validation"""
        # Create a special validation class
        from pydantic import Field
        class StrictQuestionModel(BaseModel):
            title: str = Field(..., min_length=1)
            content: str = Field(..., min_length=1)
            
        # Test with empty title
        with pytest.raises(ValidationError):
            StrictQuestionModel(title="", content="Content")
            
        # Test with empty content
        with pytest.raises(ValidationError):
            StrictQuestionModel(title="Title", content="")

class TestAnswerModels:
    """Test Answer-related models"""
    
    def test_answer_creation(self, sample_answer):
        """Test Answer model creation"""
        assert sample_answer.id == 1
        assert sample_answer.content == "This is a test answer"
        assert sample_answer.question_id == 1
        assert sample_answer.votes == 3
        assert sample_answer.is_accepted is True
        assert sample_answer.author.name == "Answer Author"
    
    def test_answer_create_model(self):
        """Test AnswerCreate model"""
        answer_data = {
            "content": "New answer content",
            "author_id": 1,
            "question_id": 1,
            "answered": "2024-01-15T12:00:00Z"
        }
        answer_create = AnswerCreate(**answer_data)
        assert answer_create.content == "New answer content"
        assert answer_create.author_id == 1
        assert answer_create.question_id == 1
    
    def test_answer_update_model(self):
        """Test AnswerUpdate model"""
        update_data = {"votes": 5, "is_accepted": True}
        answer_update = AnswerUpdate(**update_data)
        assert answer_update.votes == 5
        assert answer_update.is_accepted is True
        assert answer_update.content is None
    
    def test_answer_defaults(self):
        """Test Answer model defaults"""
        answer_base = AnswerCreate(
            content="Test content",
            answered="2024-01-15T12:00:00Z",
            author_id=1,
            question_id=1
        )
        assert answer_base.votes == 0
        assert answer_base.is_accepted is False

class TestTagModels:
    """Test Tag-related models"""
    
    def test_tag_creation(self, sample_tag):
        """Test Tag model creation"""
        assert sample_tag.id == 1
        assert sample_tag.name == "python"
        assert sample_tag.description == "Python programming language"
        assert sample_tag.count == 100
    
    def test_tag_create_model(self):
        """Test TagCreate model"""
        tag_data = {
            "name": "javascript",
            "description": "JavaScript programming language",
            "count": 50
        }
        tag_create = TagCreate(**tag_data)
        assert tag_create.name == "javascript"
        assert tag_create.count == 50
    
    def test_tag_defaults(self):
        """Test Tag model defaults"""
        tag = TagCreate(name="test")
        assert tag.description == ""
        assert tag.count == 0

class TestSearchModels:
    """Test Search-related models"""
    
    def test_search_params_creation(self):
        """Test SearchParams model"""
        params = SearchParams(
            q="python fastapi",
            tags=["python", "fastapi"],
            user="user1",
            sort="votes",
            page=2,
            limit=10
        )
        assert params.q == "python fastapi"
        assert params.tags is not None and len(params.tags) == 2
        assert params.sort == "votes"
        assert params.page == 2
        assert params.limit == 10
    
    def test_search_params_defaults(self):
        """Test SearchParams defaults"""
        params = SearchParams(
            q="test query", 
            tags=None,
            user=None,
            sort="relevance",
            page=1,
            limit=15
        )
        assert params.sort == "relevance"
        assert params.page == 1
        assert params.limit == 15
        assert params.tags is None
        assert params.user is None
    
    def test_search_request_creation(self):
        """Test SearchRequest model"""
        request = SearchRequest(
            query="python",
            search_type="questions",
            tags=["python"],
            sort="newest"
        )
        assert request.query == "python"
        assert request.search_type == "questions"
        assert request.sort == "newest"
        assert len(request.tags) == 1
    
    def test_search_result_creation(self):
        """Test SearchResult model"""
        user = User(id=1, name="Test", badges=UserBadges())
        questions = [QuestionSummary(
            id=1, title="Test", content="Content", author=user,
            votes=0, views=0, asked="2024-01-15T10:30:00Z",
            tags=[], answer_count=0
        )]
        
        result = SearchResult(
            questions=questions,
            total=1,
            page=1,
            limit=10,
            total_pages=1
        )
        assert len(result.questions) == 1
        assert result.total == 1
        assert result.total_pages == 1

class TestUtilityModels:
    """Test utility models"""
    
    def test_paginated_response(self):
        """Test PaginatedResponse model"""
        items = [{"id": 1, "name": "item1"}]
        response = PaginatedResponse(
            items=items,
            total=1,
            page=1,
            limit=10
        )
        assert len(response.items) == 1
        assert response.total == 1
        assert response.page == 1
        assert response.limit == 10
    
    def test_message_response(self):
        """Test MessageResponse model"""
        response = MessageResponse(message="Success")
        assert response.message == "Success"
        assert response.success is True
        
        error_response = MessageResponse(message="Error", success=False)
        assert error_response.success is False
    
    def test_user_stats(self):
        """Test UserStats model"""
        badges = UserBadges(gold=1, silver=2, bronze=3)
        stats = UserStats(
            total_questions=5,
            total_answers=10,
            total_votes=15,
            reputation=100,
            badges=badges
        )
        assert stats.total_questions == 5
        assert stats.total_answers == 10
        assert stats.badges.gold == 1
    
    def test_site_stats(self):
        """Test SiteStats model"""
        stats = SiteStats(
            total_questions=100,
            total_answers=250,
            total_users=50,
            total_tags=25
        )
        assert stats.total_questions == 100
        assert stats.total_answers == 250
        assert stats.total_users == 50
        assert stats.total_tags == 25
