from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr, constr, validator
from datetime import datetime
import re

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class UserAuth(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=255)

    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: str

# User models
class UserBadges(BaseModel):
    gold: int = Field(default=0, ge=0)
    silver: int = Field(default=0, ge=0)
    bronze: int = Field(default=0, ge=0)

class UserProfile(BaseModel):
    basic: Optional[dict] = Field(default_factory=lambda: {
        "displayName": "",
        "location": "",
        "title": "",
        "pronouns": "",
    })
    about: Optional[dict] = Field(default_factory=lambda: {
        "bio": "",
        "interests": "",
    })
    developer: Optional[dict] = Field(default_factory=lambda: {
        "primaryLanguage": "",
        "technologies": "",
        "yearsOfExperience": "",
        "githubProfile": "",
    })
    links: Optional[dict] = Field(default_factory=lambda: {
        "website": "",
        "twitter": "",
        "github": "",
    })

class UserBase(BaseModel):
    name: constr(min_length=3, max_length=50)
    email: EmailStr
    reputation: int = Field(default=0, ge=0)
    avatar: str = Field(default="", max_length=255)
    location: Optional[constr(max_length=100)] = None
    website: Optional[constr(max_length=255)] = None
    is_active: bool = True
    profile: Optional[UserProfile] = None

    @validator('website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v

    class Config:
        from_attributes = True

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
    author: UserBase
    tags: List[str] = []
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
