from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Table, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    reputation = Column(Integer, default=0, nullable=False)
    location = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    about = Column(Text, nullable=True)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    questions = relationship("Question", back_populates="author", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="author", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    votes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    is_answered = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    tags = relationship("Tag", secondary="question_tags", back_populates="questions")
    question_votes = relationship("Vote", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    votes = Column(Integer, default=0)
    is_accepted = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    answer_votes = relationship("Vote", back_populates="answer")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    count = Column(Integer, default=0)
    
    # Relationships
    questions = relationship("Question", secondary="question_tags", back_populates="tags")

# Association tables
question_tags = Table(
    "question_tags",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=True)
    vote_type = Column(String)  # "up" or "down"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="votes")
    question = relationship("Question", back_populates="question_votes")
    answer = relationship("Answer", back_populates="answer_votes")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    type = Column(String)  # gold, silver, bronze
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    awarded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="users")

class AnalyticsLog(Base):
    __tablename__ = "analytics_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    event_type = Column(String)
    event_data = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User") 