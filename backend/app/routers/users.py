from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db.db import get_db
from ..db import models as db_models
from ..data_service import DataService
from ..models import User, PaginatedResponse, UserCreate, UserUpdate, UserStats, UserProfile

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=PaginatedResponse[User])
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search users by name or location"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.get_users(page=page, limit=limit, search=search)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    user = data_service.get_user_by_id(user_id)
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
    user = data_service.get_user_by_id(user_id)
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
    user = data_service.get_user_by_id(user_id)
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
    user = data_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}/profile", response_model=User)
async def update_user_profile(
    user_id: int,
    profile: UserProfile,
    db: Session = Depends(get_db)
):
    """Update a user's profile information"""
    data_service = DataService(db)
    user = data_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get the actual database user object to update the profile
    db_user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the profile JSON field
    setattr(db_user, 'profile', profile.dict())
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    user = data_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
