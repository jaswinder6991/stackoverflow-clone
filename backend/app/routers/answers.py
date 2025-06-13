from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db.db import get_db
from ..data_service import DataService
from ..models import Answer, AnswerCreate, AnswerUpdate

router = APIRouter(
    prefix="/answers",
    tags=["answers"]
)

@router.get("/", response_model=List[Answer])
async def get_answers(
    question_id: Optional[int] = None,
    user_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("votes", description="Sort by: votes, newest, oldest"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.get_answers(
        question_id=question_id,
        user_id=user_id,
        page=page,
        limit=limit,
        sort=sort or "votes"
    )

@router.get("/{answer_id}", response_model=Answer)
async def get_answer(
    answer_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    answer = data_service.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.post("/", response_model=Answer)
async def create_answer(
    answer: AnswerCreate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.create_answer(
        question_id=answer.question_id,
        user_id=answer.user_id,
        content=answer.content
    )

@router.put("/{answer_id}", response_model=Answer)
async def update_answer(
    answer_id: int,
    answer_update: AnswerUpdate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    answer = data_service.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    # Update answer fields
    for field, value in answer_update.dict(exclude_unset=True).items():
        setattr(answer, field, value)
    
    db.commit()
    db.refresh(answer)
    return answer

@router.delete("/{answer_id}")
async def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    answer = data_service.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db.delete(answer)
    db.commit()
    return {"message": "Answer deleted successfully"}

@router.post("/{answer_id}/vote")
async def vote_answer(
    answer_id: int,
    user_id: int,
    vote_type: str = Query(..., description="Vote type: up or down"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    answer = data_service.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if vote_type not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    data_service.vote_answer(answer_id, user_id, vote_type)
    return {"message": "Vote recorded successfully"}