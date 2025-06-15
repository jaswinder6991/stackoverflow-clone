from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.db import get_db
from ..db import models as db_models
from ..data_service import DataService
from ..models import Question, QuestionSummary, QuestionCreate, QuestionUpdate, MessageResponse, PaginatedResponse
import math

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

@router.get("/", response_model=PaginatedResponse)
async def get_questions(
    skip: int = Query(0, ge=0, description="Number of questions to skip"),
    limit: int = Query(15, ge=1, le=100, description="Number of questions to return"),
    sort: str = Query("newest", description="Sort by: newest, votes, active"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get a list of questions with optional filtering and sorting"""
    
    data_service = DataService(db)
    
    # Convert skip to page for data service calls
    page = (skip // limit) + 1 if limit > 0 else 1
    
    if tag:
        paginated_result = data_service.get_questions_by_tag(tag, page=page, limit=limit)
        questions_data = paginated_result.items
    elif user_id:
        paginated_result = data_service.get_questions_by_user(user_id, page=page, limit=limit)
        questions_data = paginated_result.items
    else:
        questions_data = data_service.get_questions(skip=skip, limit=limit, sort=sort)
    
    total = db.query(db_models.Question).count()
    
    questions = []
    for q_data in questions_data:
        question = QuestionSummary(
            id=q_data.id,
            title=q_data.title,
            content=q_data.body[:200] + "..." if len(q_data.body) > 200 else q_data.body,
            author=q_data.author,
            tags=[t.name for t in q_data.tags],
            votes=q_data.votes,
            views=q_data.views,
            answer_count=len(q_data.answers),
            asked=q_data.created_at
        )
        questions.append(question)
    
    return {
        "items": questions,
        "total": total,
        "page": skip // limit + 1,
        "limit": limit
    }

@router.get("/search", response_model=List[QuestionSummary])
async def search_questions(
    q: str = Query(..., description="Search query"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"), 
    skip: int = Query(0, ge=0),
    limit: int = Query(15, ge=1, le=100),
    sort: str = Query("relevance", description="Sort by: relevance, newest, votes, active"),
    db: Session = Depends(get_db)
):
    """Search questions"""
    
    data_service = DataService(db)
    
    questions_data, total = data_service.search_questions(
        query=q,
        tags=tags or [],
        skip=skip,
        limit=limit,
        sort=sort
    )
    
    questions = []
    for q_data in questions_data:
        question = QuestionSummary(
            id=q_data["id"],
            title=q_data["title"],
            content=q_data["content"][:200] + "..." if len(q_data["content"]) > 200 else q_data["content"],
            author=q_data["author"],
            tags=q_data["tags"],
            votes=q_data["votes"],
            views=q_data["views"],
            answer_count=q_data.get("answer_count", 0),
            asked=q_data["asked"]
        )
        questions.append(question)
    
    return questions

@router.get("/{question_id}", response_model=Question)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific question with its answers"""
    
    data_service = DataService(db)
    
    # Increment view count
    data_service.increment_question_views(question_id)
    
    question_data = data_service.get_question_by_id(question_id)
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Return the question object directly since get_question_by_id returns a Question object
    return question_data

@router.post("/", response_model=None)  # Remove response_model constraint for debugging
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Create a new question"""
    data_service = DataService(db)
    
    # Verify user exists
    user_data = data_service.get_user_by_id(question.author_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_question = data_service.create_question(question, question.author_id)
    # Convert to a dict and manually select fields that match the Pydantic model
    return {
        "id": db_question.id,
        "title": db_question.title,
        "body": db_question.body,
        "author_id": db_question.author_id,
        "created_at": db_question.created_at,
        "updated_at": db_question.updated_at,
        "votes": db_question.votes,
        "views": db_question.views,
        "is_answered": db_question.is_answered
    }

@router.put("/{question_id}", response_model=Question)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """Update a question (mock implementation)"""
    data_service = DataService(db)
    
    question_data = data_service.get_question_by_id(question_id)
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question = data_service.get_question(question_id)
    
    # Update question fields
    for field, value in question_update.dict(exclude_unset=True).items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    return question

@router.delete("/{question_id}", response_model=MessageResponse)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question (mock implementation)"""
    data_service = DataService(db)
    
    question_data = data_service.get_question_by_id(question_id)
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    data_service.delete_question(question_id)
    
    return MessageResponse(
        message=f"Question {question_id} would be deleted",
        success=True
    )

@router.post("/{question_id}/vote")
async def vote_question(
    question_id: int,
    user_id: int,
    vote_type: str = Query(..., description="Vote type: up or down"),
    db: Session = Depends(get_db)
):
    """Vote on a question"""
    data_service = DataService(db)
    
    question_data = data_service.get_question_by_id(question_id)
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if vote_type not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    data_service.vote_question(question_id, user_id, vote_type)
    return {"message": "Vote recorded successfully"}

@router.get("/tagged/{tag}", response_model=List[QuestionSummary])
async def get_questions_tagged(
    tag: str,
    skip: int = Query(0, ge=0, description="Number of questions to skip"),
    limit: int = Query(15, ge=1, le=100, description="Number of questions to return"),
    sort: str = Query("newest", description="Sort by: newest, votes, active"),
    db: Session = Depends(get_db)
):
    """Get questions filtered by a specific tag"""
    
    data_service = DataService(db)
    
    # Convert skip to page for data service calls
    page = (skip // limit) + 1 if limit > 0 else 1
    
    paginated_result = data_service.get_questions_by_tag(tag, page=page, limit=limit)
    questions_data = paginated_result.items
    
    questions = []
    for q_data in questions_data:
        question = QuestionSummary(
            id=q_data["id"],
            title=q_data["title"],
            content=q_data["content"][:200] + "..." if len(q_data["content"]) > 200 else q_data["content"],
            author=q_data["author"],
            tags=q_data["tags"],
            votes=q_data["votes"],
            views=q_data["views"],
            answer_count=q_data.get("answer_count", 0),
            asked=q_data["asked"]
        )
        questions.append(question)
    
    return questions
