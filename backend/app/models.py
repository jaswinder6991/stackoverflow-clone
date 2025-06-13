from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# User models
class UserBadges(BaseModel):
    gold: int = 0
    silver: int = 0
    bronze: int = 0

class UserBase(BaseModel):
    name: str
    email: EmailStr
    reputation: int = 0
    avatar: str = ""
    location: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Answer models
class AnswerBase(BaseModel):
    body: str

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    author_id: int
    answered: datetime

    class Config:
        from_attributes = True

# Question models  
class QuestionBase(BaseModel):
    title: str
    body: str

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    author_id: int
    asked: datetime
    modified: datetime

    class Config:
        from_attributes = True
    
class QuestionSummary(BaseModel):
    """Simplified question model for listing pages"""
    id: int
    title: str
    content: str  # Will be truncated
    author_id: int
    votes: int
    views: int
    asked: datetime
    answer_count: int

    class Config:
        from_attributes = True

class QuestionTag(BaseModel):
    question_id: int
    tag_id: int

    class Config:
        from_attributes = True

# Tag models
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

# Search models
class SearchParams(BaseModel):
    q: str = Field(..., description="Search query")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    user: Optional[str] = Field(None, description="Filter by user")
    sort: Optional[str] = Field("relevance", description="Sort by: relevance, votes, newest, active")
    page: Optional[int] = Field(1, description="Page number")
    limit: Optional[int] = Field(15, description="Items per page")

class SearchResult(BaseModel):
    questions: List[QuestionSummary]
    total: int
    page: int
    limit: int
    total_pages: int

# Statistics models
class UserStats(BaseModel):
    total_questions: int
    total_answers: int
    total_votes: int
    reputation: int
    badges: UserBadges

class SiteStats(BaseModel):
    total_questions: int
    total_answers: int
    total_users: int
    total_tags: int

# Response models
class MessageResponse(BaseModel):
    message: str
    success: bool = True

# Generic models
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    
class SearchRequest(BaseModel):
    query: str
    page: int = 1
    page_size: int = 10

class SearchResponse(BaseModel):
    results: List[Question]
    total: int
    page: int
    page_size: int
    total_pages: int
