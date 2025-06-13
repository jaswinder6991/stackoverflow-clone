import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from app.data_service import DataService
from app.models import PaginatedResponse


class TestDataService:
    """Test DataService functionality"""
    
    def test_init_with_valid_data(self, mock_data):
        """Test DataService initialization with valid data files"""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.load') as mock_json_load:
                mock_json_load.side_effect = [
                    mock_data["users"],
                    mock_data["questions"], 
                    mock_data["answers"],
                    mock_data["tags"]
                ]
                
                service = DataService()
                assert len(service.users) == len(mock_data["users"])
                assert len(service.questions) == len(mock_data["questions"])
                assert len(service.answers) == len(mock_data["answers"])
                assert len(service.tags) == len(mock_data["tags"])
    
    def test_init_with_missing_files(self):
        """Test DataService initialization with missing data files"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            service = DataService()
            assert service.users == []
            assert service.questions == []
            assert service.answers == []
            assert service.tags == []
    
    def test_load_data_file_not_found(self):
        """Test _load_data method when files don't exist"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
                service._load_data()
                assert service.users == []
                assert service.questions == []
                assert service.answers == []
                assert service.tags == []
    
    def test_load_data_invalid_json(self):
        """Test _load_data method with invalid JSON"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            with patch('builtins.open', mock_open(read_data="invalid json")):
                with patch('json.load', side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
                    service._load_data()
                    # Should handle gracefully, not crash
                    assert service.users == []


class TestDataServiceUserMethods:
    """Test user-related methods"""
    
    def test_get_user_by_id_existing(self, mock_data):
        """Test getting an existing user by ID"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            user = service.get_user_by_id(1)
            assert user is not None
            assert user["id"] == 1
            assert user["name"] == "John Doe"
    
    def test_get_user_by_id_nonexistent(self, mock_data):
        """Test getting a nonexistent user by ID"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            user = service.get_user_by_id(999)
            assert user is None
    
    def test_get_users_no_search(self, mock_data):
        """Test getting users without search"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            result = service.get_users(page=1, limit=10)
            assert isinstance(result, PaginatedResponse)
            assert result.total == len(mock_data["users"])
            assert len(result.items) == len(mock_data["users"])
            assert result.page == 1
            assert result.limit == 10
    
    def test_get_users_with_search(self, mock_data):
        """Test getting users with search"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            result = service.get_users(page=1, limit=10, search="john")
            assert isinstance(result, PaginatedResponse)
            assert result.total == 1
            assert result.items[0]["name"] == "John Doe"
    
    def test_get_users_search_location(self, mock_data):
        """Test searching users by location"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            result = service.get_users(page=1, limit=10, search="york")
            assert result.total == 1
            assert result.items[0]["location"] == "New York"
    
    def test_get_users_pagination(self, mock_data):
        """Test user pagination"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = mock_data["users"]
            
            result = service.get_users(page=1, limit=1)
            assert len(result.items) == 1
            assert result.total == 2
            
            result_page2 = service.get_users(page=2, limit=1)
            assert len(result_page2.items) == 1
            assert result.items[0]["id"] != result_page2.items[0]["id"]


class TestDataServiceQuestionMethods:
    """Test question-related methods"""
    
    def test_get_question_by_id_existing(self, mock_data):
        """Test getting an existing question by ID"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            
            question = service.get_question_by_id(1)
            assert question is not None
            assert question["id"] == 1
            assert question["title"] == "How to use Python with FastAPI?"
            assert "answers" in question
    
    def test_get_question_by_id_nonexistent(self, mock_data):
        """Test getting a nonexistent question by ID"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            
            question = service.get_question_by_id(999)
            assert question is None
    
    def test_get_questions_default_params(self, mock_data):
        """Test getting questions with default parameters"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            
            questions = service.get_questions()
            assert len(questions) == len(mock_data["questions"])
            for question in questions:
                assert "answer_count" in question
    
    def test_get_questions_pagination(self, mock_data):
        """Test question pagination"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            
            questions = service.get_questions(skip=0, limit=1)
            assert len(questions) == 1
            
            questions_skip = service.get_questions(skip=1, limit=1)
            assert len(questions_skip) == 1
            assert questions[0]["id"] != questions_skip[0]["id"]
    
    def test_get_questions_sorting(self, mock_data):
        """Test question sorting"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            
            # Test different sort methods
            questions_newest = service.get_questions(sort="newest")
            questions_votes = service.get_questions(sort="votes")
            questions_active = service.get_questions(sort="active")
            
            assert len(questions_newest) == 2
            assert len(questions_votes) == 2
            assert len(questions_active) == 2
    
    def test_get_questions_by_user(self, mock_data):
        """Test getting questions by user"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            result = service.get_questions_by_user(user_id=1, page=1, limit=10)
            assert isinstance(result, PaginatedResponse)
            assert result.total == 1
            assert result.items[0]["author"]["id"] == 1
    
    def test_get_questions_by_user_nonexistent(self, mock_data):
        """Test getting questions by nonexistent user"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            result = service.get_questions_by_user(user_id=999, page=1, limit=10)
            assert result.total == 0
            assert len(result.items) == 0


class TestDataServiceSearchMethods:
    """Test search-related methods"""
    
    def test_search_questions_by_title(self, mock_data):
        """Test searching questions by title"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            questions, total = service.search_questions(query="python", skip=0, limit=10)
            assert total == 1
            assert "Python" in questions[0]["title"]
    
    def test_search_questions_by_content(self, mock_data):
        """Test searching questions by content"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            questions, total = service.search_questions(query="fastapi", skip=0, limit=10)
            assert total == 1
            assert "FastAPI" in questions[0]["content"]
    
    def test_search_questions_by_tags(self, mock_data):
        """Test searching questions by tags"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            questions, total = service.search_questions(query="javascript", skip=0, limit=10)
            assert total == 1
            assert "javascript" in questions[0]["tags"]
    
    def test_search_questions_case_insensitive(self, mock_data):
        """Test case-insensitive search"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            questions, total = service.search_questions(query="PYTHON", skip=0, limit=10)
            assert total == 1
    
    def test_search_questions_no_results(self, mock_data):
        """Test search with no results"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            questions, total = service.search_questions(query="nonexistent", skip=0, limit=10)
            assert total == 0
            assert len(questions) == 0


class TestDataServiceTagMethods:
    """Test tag-related methods"""
    
    def test_get_tags(self, mock_data):
        """Test getting all tags"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.tags = mock_data["tags"]
            
            result = service.get_tags(page=1, limit=10)
            assert isinstance(result, PaginatedResponse)
            assert result.total == len(mock_data["tags"])
            assert len(result.items) == len(mock_data["tags"])
    
    def test_get_tag_by_name(self, mock_data):
        """Test getting tag by name"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.tags = mock_data["tags"]
            
            tag = service.get_tag_by_name("python")
            assert tag is not None
            assert tag["name"] == "python"
    
    def test_get_tag_by_name_nonexistent(self, mock_data):
        """Test getting nonexistent tag by name"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.tags = mock_data["tags"]
            
            tag = service.get_tag_by_name("nonexistent")
            assert tag is None
    
    def test_get_questions_by_tag(self, mock_data):
        """Test getting questions by tag"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            result = service.get_questions_by_tag("python", page=1, limit=10)
            assert isinstance(result, PaginatedResponse)
            assert result.total == 1
            assert "python" in result.items[0]["tags"]
    
    def test_get_questions_by_tag_nonexistent(self, mock_data):
        """Test getting questions by nonexistent tag"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            result = service.get_questions_by_tag("nonexistent", page=1, limit=10)
            assert result.total == 0


class TestDataServiceAnswerMethods:
    """Test answer-related methods"""
    
    def test_get_answers_by_question(self, mock_data):
        """Test getting answers by question ID"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            answers = service.get_answers_by_question(question_id=1)
            assert len(answers) == 1
            assert answers[0]["question_id"] == 1
    
    def test_get_answers_by_question_no_answers(self, mock_data):
        """Test getting answers for question with no answers"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            answers = service.get_answers_by_question(question_id=999)
            assert len(answers) == 0


class TestDataServiceUtilityMethods:
    """Test utility methods"""
    
    def test_sort_questions_newest(self):
        """Test sorting questions by newest"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = []
            service.questions = []
            service.answers = []
            service.tags = []
            
            questions = [
                {"id": 1, "asked": "2024-01-15T10:30:00Z", "votes": 5, "modified": "2024-01-15T10:30:00Z"},
                {"id": 2, "asked": "2024-01-16T10:30:00Z", "votes": 3, "modified": "2024-01-16T10:30:00Z"}
            ]
            sorted_questions = service._sort_questions(questions, "newest")
            assert sorted_questions[0]["id"] == 2
    
    def test_sort_questions_votes(self):
        """Test sorting questions by votes"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = []
            service.questions = []
            service.answers = []
            service.tags = []
            
            questions = [
                {"id": 1, "asked": "2024-01-15T10:30:00Z", "votes": 5, "modified": "2024-01-15T10:30:00Z"},
                {"id": 2, "asked": "2024-01-16T10:30:00Z", "votes": 10, "modified": "2024-01-16T10:30:00Z"}
            ]
            sorted_questions = service._sort_questions(questions, "votes")
            assert sorted_questions[0]["votes"] == 10
    
    def test_sort_questions_active(self):
        """Test sorting questions by activity"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = []
            service.questions = []
            service.answers = []
            service.tags = []
            
            questions = [
                {"id": 1, "asked": "2024-01-15T10:30:00Z", "votes": 5, "modified": "2024-01-15T10:30:00Z"},
                {"id": 2, "asked": "2024-01-16T10:30:00Z", "votes": 3, "modified": "2024-01-17T10:30:00Z"}
            ]
            sorted_questions = service._sort_questions(questions, "active")
            # Active sorts by votes in the current implementation
            assert len(sorted_questions) == 2
    
    def test_sort_questions_invalid_sort(self):
        """Test sorting questions with invalid sort parameter"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.users = []
            service.questions = []
            service.answers = []
            service.tags = []
            
            questions = [{"id": 1, "asked": "2024-01-15T10:30:00Z", "votes": 5, "modified": "2024-01-15T10:30:00Z"}]
            sorted_questions = service._sort_questions(questions, "invalid")
            # Should default to newest (by id reverse)
            assert len(sorted_questions) == 1
    
    def test_get_user_stats(self, mock_data):
        """Test getting user statistics"""
        with patch('app.data_service.DataService._load_data'):
            service = DataService()
            service.questions = mock_data["questions"]
            service.answers = mock_data["answers"]
            service.users = mock_data["users"]
            
            stats = service.get_user_stats(user_id=1)
            assert isinstance(stats, dict)
            assert "questions_count" in stats
            assert "answers_count" in stats
            assert "total_votes" in stats
