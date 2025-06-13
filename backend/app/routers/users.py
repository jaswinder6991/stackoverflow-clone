from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db.db import get_db
from ..data_service import DataService
from ..models import User, PaginatedResponse, UserCreate, UserUpdate, UserStats

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    user = data_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/questions", response_model=PaginatedResponse)
async def get_user_questions(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get questions posted by a specific user"""
    data_service = DataService(db)
    # Check if user exists
    user = data_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    questions = data_service.get_questions_by_user(user_id, page=page, limit=limit)
    return questions

@router.get("/{user_id}/answers", response_model=PaginatedResponse)
async def get_user_answers(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get answers posted by a specific user"""
    data_service = DataService(db)
    # Check if user exists
    user = data_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    answers = data_service.get_answers_by_user(user_id, page=page, limit=limit)
    return answers

@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    stats = data_service.get_user_stats(user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats

@router.post("/", response_model=User)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.create_user(
        name=user.name,
        email=user.email,
        hashed_password=user.password
    )

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    user = data_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    user = data_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
