import json
import os
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete
from .db.models import User, Question, Answer, Tag
from .models import QuestionSummary, PaginatedResponse, SearchRequest, SearchResponse
import math
from datetime import datetime
from sqlalchemy import func
from .db.models import question_tags
from .models import QuestionCreate, AnswerCreate, TagCreate, UserCreate

class DataService:
    def __init__(self, db: Session):
        self.db = db
        self.data_dir = "data"
        self.users: List[Dict] = []
        self.questions: List[Dict] = []
        self.answers: List[Dict] = []
        self.tags: List[Dict] = []
        self._load_data()
    
    def _load_data(self):
        """Load all JSON data files into memory"""
        try:
            # Load users
            with open(os.path.join(self.data_dir, "users.json"), "r") as f:
                self.users = json.load(f)
            
            # Load questions  
            with open(os.path.join(self.data_dir, "questions.json"), "r") as f:
                self.questions = json.load(f)
            
            # Load answers
            with open(os.path.join(self.data_dir, "answers.json"), "r") as f:
                self.answers = json.load(f)
                
            # Load tags
            with open(os.path.join(self.data_dir, "tags.json"), "r") as f:
                self.tags = json.load(f)
                
            print(f"Loaded {len(self.users)} users, {len(self.questions)} questions, {len(self.answers)} answers, {len(self.tags)} tags")
            
        except FileNotFoundError as e:
            print(f"Data file not found: {e}")
            self.users = []
            self.questions = []
            self.answers = []
            self.tags = []
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_users(self, page: int = 1, limit: int = 20, search: Optional[str] = None) -> PaginatedResponse:
        """Get paginated list of users with optional search"""
        query = self.db.query(User)
        
        if search:
            query = query.filter(
                (User.name.ilike(f"%{search}%")) |
                (User.location.ilike(f"%{search}%"))
            )
        
        total = query.count()
        users = query.offset((page - 1) * limit).limit(limit).all()
        
        return PaginatedResponse(
            items=users,
            total=total,
            page=page,
            limit=limit
        )
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """Get question by ID with answers"""
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if question:
            # Add answers to question
            question.answers = self.get_answers(question_id)
            return question
        return None
    
    def get_questions(self, skip: int = 0, limit: int = 10, sort: str = "newest") -> List[Question]:
        """Get a list of questions with pagination"""
        query = self.db.query(Question)
        
        if sort == "newest":
            query = query.order_by(Question.created_at.desc())
        elif sort == "votes":
            query = query.order_by(Question.votes.desc())
        elif sort == "active":
            query = query.order_by(Question.updated_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def get_total_questions(self) -> int:
        """Get total number of questions"""
        return self.db.query(Question).count()
    
    def get_questions_by_user(self, user_id: int, page: int = 1, limit: int = 15) -> PaginatedResponse:
        """Get questions by user with pagination"""
        query = self.db.query(Question).filter(Question.author_id == user_id)
        total = query.count()
        questions = query.offset((page - 1) * limit).limit(limit).all()
        
        return PaginatedResponse(
            items=questions,
            total=total,
            page=page,
            limit=limit
        )
    
    def get_answers_by_user(self, user_id: int, page: int = 1, limit: int = 15) -> PaginatedResponse:
        """Get answers by user with pagination"""
        query = self.db.query(Answer).filter(Answer.author_id == user_id)
        total = query.count()
        answers = query.offset((page - 1) * limit).limit(limit).all()
        
        return PaginatedResponse(
            items=answers,
            total=total,
            page=page,
            limit=limit
        )
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        user_questions = self.db.query(Question).filter(Question.author_id == user_id).count()
        user_answers = self.db.query(Answer).filter(Answer.author_id == user_id).count()
        
        # Calculate total votes received
        question_votes = self.db.query(Question).filter(Question.author_id == user_id).with_entities(func.sum(Question.votes)).scalar() or 0
        answer_votes = self.db.query(Answer).filter(Answer.author_id == user_id).with_entities(func.sum(Answer.votes)).scalar() or 0
        
        return {
            "questions_count": user_questions,
            "answers_count": user_answers,
            "total_votes": question_votes + answer_votes,
            "question_votes": question_votes,
            "answer_votes": answer_votes
        }
    
    def get_answers_by_question(self, question_id: int) -> List[Answer]:
        """Get all answers for a question"""
        return self.db.query(Answer).filter(Answer.question_id == question_id).all()
    
    def get_tags(self) -> List[Tag]:
        """Get all tags"""
        return self.db.query(Tag).all()
    
    def get_tag_by_name(self, tag_name: str) -> Optional[Tag]:
        """Get tag by name"""
        return self.db.query(Tag).filter(Tag.name.ilike(tag_name)).first()
    
    def get_questions_by_tag(self, tag_name: str, page: int = 1, limit: int = 15, sort: str = "newest") -> PaginatedResponse:
        """Get questions filtered by tag with pagination"""
        tag = self.get_tag_by_name(tag_name)
        if not tag:
            return PaginatedResponse(items=[], total=0, page=page, limit=limit)
        
        query = self.db.query(Question).filter(Question.tags.contains([tag_name]))
        
        if sort == "newest":
            query = query.order_by(Question.created_at.desc())
        elif sort == "votes":
            query = query.order_by(Question.votes.desc())
        elif sort == "active":
            query = query.order_by(Question.updated_at.desc())
        
        total = query.count()
        questions = query.offset((page - 1) * limit).limit(limit).all()
        
        return PaginatedResponse(
            items=questions,
            total=total,
            page=page,
            limit=limit
        )
    
    def get_popular_tags(self, limit: int = 20) -> List[Tag]:
        """Get most popular tags"""
        return self.db.query(Tag).order_by(Tag.count.desc()).limit(limit).all()
    
    def get_trending_tags(self, limit: int = 10) -> List[Tag]:
        """Get trending tags (for demo, return most popular)"""
        return self.get_popular_tags(limit)
    
    def search_questions(self, query: str, tags: List[str] = None, skip: int = 0, limit: int = 20, sort: str = "relevance") -> tuple[List[Question], int]:
        """Search questions by title or content"""
        search_query = self.db.query(Question).filter(
            (Question.title.ilike(f"%{query}%")) | (Question.content.ilike(f"%{query}%"))
        )
        
        if tags:
            search_query = search_query.filter(Question.tags.overlap(tags))
        
        if sort == "relevance":
            # For now, just sort by newest
            search_query = search_query.order_by(Question.created_at.desc())
        elif sort == "newest":
            search_query = search_query.order_by(Question.created_at.desc())
        elif sort == "votes":
            search_query = search_query.order_by(Question.votes.desc())
        
        total = search_query.count()
        questions = search_query.offset(skip).limit(limit).all()
        
        return questions, total
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.name == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, name: str, email: str, hashed_password: str) -> User:
        """Create a new user"""
        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """Get question by ID"""
        return self.db.query(Question).filter(Question.id == question_id).first()
    
    def create_question(self, question: QuestionCreate, author_id: int) -> Question:
        """Create a new question"""
        db_question = Question(
            title=question.title,
            body=question.body,
            author_id=author_id,
            asked=datetime.utcnow(),
            modified=datetime.utcnow()
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question
    
    def get_answers(self, question_id: int) -> List[Answer]:
        """Get all answers for a question"""
        return self.db.query(Answer).filter(Answer.question_id == question_id).all()
    
    def create_answer(self, answer: AnswerCreate, question_id: int, author_id: int) -> Answer:
        """Create a new answer"""
        db_answer = Answer(
            body=answer.body,
            question_id=question_id,
            author_id=author_id,
            answered=datetime.utcnow()
        )
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return db_answer
    
    def vote_question(self, question_id: int, user_id: int, vote_type: str):
        """Vote on a question"""
        question = self.get_question(question_id)
        if not question:
            raise ValueError("Question not found")
        
        if vote_type == "up":
            question.votes += 1
        elif vote_type == "down":
            question.votes -= 1
        
        self.db.commit()
    
    def vote_answer(self, answer_id: int, user_id: int, vote_type: str):
        """Vote on an answer"""
        answer = self.db.query(Answer).filter(Answer.id == answer_id).first()
        if not answer:
            raise ValueError("Answer not found")
        
        if vote_type == "up":
            answer.votes += 1
        elif vote_type == "down":
            answer.votes -= 1
        
        self.db.commit()
    
    def increment_question_views(self, question_id: int):
        """Increment question view count"""
        question = self.get_question(question_id)
        if question:
            question.views += 1
            self.db.commit()
    
    def get_site_stats(self) -> Dict[str, int]:
        """Get site statistics"""
        return {
            "total_questions": self.db.query(Question).count(),
            "total_answers": self.db.query(Answer).count(),
            "total_users": self.db.query(User).count(),
            "total_tags": self.db.query(Tag).count()
        }

    def update_question(self, question_id: int, question: QuestionCreate) -> Optional[Question]:
        db_question = self.get_question(question_id)
        if db_question:
            db_question.title = question.title
            db_question.body = question.body
            db_question.modified = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_question)
        return db_question

    def delete_question(self, question_id: int) -> bool:
        db_question = self.get_question(question_id)
        if db_question:
            self.db.delete(db_question)
            self.db.commit()
            return True
        return False

    def get_answer(self, answer_id: int) -> Optional[Answer]:
        return self.db.query(Answer).filter(Answer.id == answer_id).first()

    def update_answer(self, answer_id: int, answer: AnswerCreate) -> Optional[Answer]:
        db_answer = self.get_answer(answer_id)
        if db_answer:
            db_answer.body = answer.body
            self.db.commit()
            self.db.refresh(db_answer)
        return db_answer

    def delete_answer(self, answer_id: int) -> bool:
        db_answer = self.get_answer(answer_id)
        if db_answer:
            self.db.delete(db_answer)
            self.db.commit()
            return True
        return False

    def get_tags(self, skip: int = 0, limit: int = 10) -> List[Tag]:
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def create_tag(self, tag: TagCreate) -> Tag:
        db_tag = Tag(name=tag.name)
        self.db.add(db_tag)
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag

    def update_tag(self, tag_id: int, tag: TagCreate) -> Optional[Tag]:
        db_tag = self.get_tag(tag_id)
        if db_tag:
            db_tag.name = tag.name
            self.db.commit()
            self.db.refresh(db_tag)
        return db_tag

    def delete_tag(self, tag_id: int) -> bool:
        db_tag = self.get_tag(tag_id)
        if db_tag:
            self.db.delete(db_tag)
            self.db.commit()
            return True
        return False

    def add_tag_to_question(self, question_id: int, tag_id: int) -> bool:
        question = self.get_question(question_id)
        tag = self.get_tag(tag_id)
        if question and tag:
            stmt = insert(question_tags).values(question_id=question_id, tag_id=tag_id)
            self.db.execute(stmt)
            self.db.commit()
            return True
        return False

    def remove_tag_from_question(self, question_id: int, tag_id: int) -> bool:
        stmt = delete(question_tags).where(
            question_tags.c.question_id == question_id,
            question_tags.c.tag_id == tag_id
        )
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0

    def search_questions(self, query: str, skip: int = 0, limit: int = 10) -> List[Question]:
        return self.db.query(Question).filter(
            Question.title.ilike(f"%{query}%") | Question.body.ilike(f"%{query}%")
        ).offset(skip).limit(limit).all()
