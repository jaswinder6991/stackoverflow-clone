from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.db import get_db
from app.data_service import DataService
from app.models import Comment, CommentCreate

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=Comment)
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """Create a new comment on a question or answer"""
    data_service = DataService(db)
    
    # Validate user exists
    user = data_service.get_user_by_id(comment.author_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        db_comment = data_service.create_comment(
            question_id=comment.question_id,
            answer_id=comment.answer_id,
            user_id=comment.author_id,
            content=comment.body
        )
        return db_comment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/question/{question_id}", response_model=List[Comment])
async def get_question_comments(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get all comments for a question"""
    data_service = DataService(db)
    comments = data_service.get_comments_for_question(question_id)
    return comments

@router.get("/answer/{answer_id}", response_model=List[Comment])
async def get_answer_comments(
    answer_id: int,
    db: Session = Depends(get_db)
):
    """Get all comments for an answer"""
    data_service = DataService(db)
    comments = data_service.get_comments_for_answer(answer_id)
    return comments

@router.post("/{comment_id}/vote")
async def vote_comment(
    comment_id: int,
    user_id: int = Query(..., description="ID of the user voting"),
    db: Session = Depends(get_db)
):
    """Vote on a comment (upvote only, toggle to remove)"""
    data_service = DataService(db)
    
    # Verify user exists
    user = data_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        data_service.vote_comment(comment_id, user_id)
        return {"message": "Comment vote toggled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{comment_id}/vote-status/{user_id}")
async def get_comment_vote_status(
    comment_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's vote status for a comment"""
    data_service = DataService(db)
    
    has_voted = data_service.get_user_comment_vote(comment_id, user_id)
    return {"has_voted": has_voted}
