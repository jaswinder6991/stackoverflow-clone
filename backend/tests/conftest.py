import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.data_service import DataService
from app.models import User, Question, Answer, Tag, UserBadges
from main import app
import json
import tempfile
import os

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def mock_data():
    """Create mock data for testing"""
    return {
        "users": [
            {
                "id": 1,
                "name": "John Doe",
                "reputation": 1500,
                "avatar": "https://example.com/avatar1.jpg",
                "location": "New York",
                "badges": {"gold": 2, "silver": 5, "bronze": 10}
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "reputation": 2000,
                "avatar": "https://example.com/avatar2.jpg",
                "location": "San Francisco",
                "badges": {"gold": 3, "silver": 8, "bronze": 15}
            }
        ],
        "questions": [
            {
                "id": 1,
                "title": "How to use Python with FastAPI?",
                "content": "I'm trying to learn FastAPI with Python. Can someone help me understand the basics?",
                "author": {
                    "id": 1,
                    "name": "John Doe",
                    "reputation": 1500,
                    "avatar": "https://example.com/avatar1.jpg",
                    "location": "New York",
                    "badges": {"gold": 2, "silver": 5, "bronze": 10}
                },
                "tags": ["python", "fastapi", "web-development"],
                "votes": 15,
                "views": 234,
                "asked": "2024-01-15T10:30:00Z",
                "modified": "2024-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "title": "JavaScript async/await best practices",
                "content": "What are the best practices for using async/await in JavaScript?",
                "author": {
                    "id": 2,
                    "name": "Jane Smith",
                    "reputation": 2000,
                    "avatar": "https://example.com/avatar2.jpg",
                    "location": "San Francisco",
                    "badges": {"gold": 3, "silver": 8, "bronze": 15}
                },
                "tags": ["javascript", "async", "promises"],
                "votes": 23,
                "views": 456,
                "asked": "2024-01-16T14:20:00Z",
                "modified": "2024-01-16T14:20:00Z"
            }
        ],
        "answers": [
            {
                "id": 1,
                "content": "FastAPI is a modern, fast web framework for building APIs with Python. Here's how to get started...",
                "author": {
                    "id": 2,
                    "name": "Jane Smith",
                    "reputation": 2000,
                    "avatar": "https://example.com/avatar2.jpg",
                    "location": "San Francisco",
                    "badges": {"gold": 3, "silver": 8, "bronze": 15}
                },
                "question_id": 1,
                "votes": 8,
                "is_accepted": True,
                "answered": "2024-01-15T12:00:00Z"
            },
            {
                "id": 2,
                "content": "Here are the best practices for async/await in JavaScript: 1. Always handle errors with try/catch...",
                "author": {
                    "id": 1,
                    "name": "John Doe",
                    "reputation": 1500,
                    "avatar": "https://example.com/avatar1.jpg",
                    "location": "New York",
                    "badges": {"gold": 2, "silver": 5, "bronze": 10}
                },
                "question_id": 2,
                "votes": 12,
                "is_accepted": False,
                "answered": "2024-01-16T16:30:00Z"
            }
        ],
        "tags": [
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
            },
            {
                "id": 3,
                "name": "fastapi",
                "description": "FastAPI web framework",
                "count": 45
            }
        ]
    }

@pytest.fixture
def mock_data_service(mock_data):
    """Create a mock data service with test data"""
    # Patch all the imports of data_service across the application
    patches = [
        patch('app.data_service.data_service'),
        patch('app.routers.questions.data_service'),
        patch('app.routers.users.data_service'),
        patch('app.routers.tags.data_service'),
        patch('app.routers.search.data_service'),
        patch('app.routers.answers.data_service'),
    ]
    
    mock_service = Mock()
    
    # Setup mock data
    mock_service.users = mock_data["users"]
    mock_service.questions = mock_data["questions"]
    mock_service.answers = mock_data["answers"]
    mock_service.tags = mock_data["tags"]
    
    # Mock methods with proper return types
    mock_service.get_user_by_id.side_effect = lambda user_id: next(
        (user for user in mock_data["users"] if user["id"] == user_id), None
    )
    
    mock_service.get_question_by_id.side_effect = lambda question_id: next(
        (q for q in mock_data["questions"] if q["id"] == question_id), None
    )
    
    # Fix router-specific mock methods
    mock_service.get_questions.return_value = mock_data["questions"]
    
    # Fix paginated responses 
    from app.models import PaginatedResponse
    mock_paginated = PaginatedResponse(
        items=mock_data["questions"], 
        total=len(mock_data["questions"]),
        page=1,
        limit=15
    )
    mock_service.get_questions_by_tag.return_value = mock_paginated
    mock_service.get_questions_by_user.return_value = mock_paginated
    
    # Fix search methods - return tuple format
    mock_service.search_questions.return_value = (mock_data["questions"], len(mock_data["questions"]))
    
    # Fix answers methods - return list not tuple
    mock_service.get_answers_by_question.return_value = mock_data["answers"]
    mock_service.increment_question_views = Mock()
    
    # Mock methods for other routers with proper return types
    mock_users_paginated = PaginatedResponse(
        items=mock_data["users"],
        total=len(mock_data["users"]),
        page=1,
        limit=20
    )
    mock_service.get_users.return_value = mock_users_paginated
    mock_service.get_user_stats.return_value = {
        "questions_count": 1,
        "answers_count": 1,
        "total_votes": 10,
        "question_votes": 5,
        "answer_votes": 5
    }
    
    mock_tags_paginated = PaginatedResponse(
        items=mock_data["tags"],
        total=len(mock_data["tags"]),
        page=1,
        limit=20
    )
    mock_service.get_tags.return_value = mock_tags_paginated
    mock_service.get_tag_by_name.side_effect = lambda tag_name: next(
        (tag for tag in mock_data["tags"] if tag["name"].lower() == tag_name.lower()), None
    )
    
    # Fix search service
    from app.models import SearchResponse
    mock_search_response = SearchResponse(
        query="test",
        total_results=len(mock_data["questions"]),
        questions=mock_paginated,
        users=mock_users_paginated,
        tags=mock_tags_paginated
    )
    mock_service.search.return_value = mock_search_response
    mock_service.get_answers_by_user.return_value = PaginatedResponse(
        items=mock_data["answers"],
        total=len(mock_data["answers"]),
        page=1,
        limit=15
    )
    
    # Popular/trending tags
    mock_service.get_popular_tags.return_value = mock_data["tags"][:2]
    mock_service.get_trending_tags.return_value = mock_data["tags"][:2]
    
    # Start all patches
    mocks = []
    for patch_obj in patches:
        mock_obj = patch_obj.start()
        mock_obj.return_value = mock_service
        # For patches that return the mock directly
        for attr in dir(mock_service):
            if not attr.startswith('_'):
                setattr(mock_obj, attr, getattr(mock_service, attr))
        mocks.append(mock_obj)
    
    yield mock_service
    
    # Stop all patches
    for patch_obj in patches:
        patch_obj.stop()

@pytest.fixture
def temp_data_files(mock_data):
    """Create temporary data files for testing DataService"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test data files
        for data_type, data in mock_data.items():
            file_path = os.path.join(temp_dir, f"{data_type}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f)
        
        yield temp_dir

@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    return User(
        id=1,
        name="Test User",
        reputation=100,
        avatar="https://example.com/avatar.jpg",
        location="Test City",
        badges=UserBadges(gold=1, silver=2, bronze=3)
    )

@pytest.fixture
def sample_question():
    """Create a sample question for testing"""
    return Question(
        id=1,
        title="Test Question",
        content="This is a test question content",
        author=User(
            id=1,
            name="Test User",
            reputation=100,
            avatar="https://example.com/avatar.jpg",
            badges=UserBadges()
        ),
        tags=["test", "python"],
        votes=5,
        views=100,
        asked="2024-01-15T10:30:00Z",
        modified="2024-01-15T10:30:00Z",
        answers=[]
    )

@pytest.fixture
def sample_answer():
    """Create a sample answer for testing"""
    return Answer(
        id=1,
        content="This is a test answer",
        author=User(
            id=2,
            name="Answer Author",
            reputation=200,
            avatar="https://example.com/avatar2.jpg",
            badges=UserBadges()
        ),
        question_id=1,
        votes=3,
        is_accepted=True,
        answered="2024-01-15T12:00:00Z"
    )

@pytest.fixture
def sample_tag():
    """Create a sample tag for testing"""
    return Tag(
        id=1,
        name="python",
        description="Python programming language",
        count=100
    )
