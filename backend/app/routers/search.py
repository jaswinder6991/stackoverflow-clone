from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db.db import get_db
from ..data_service import DataService
from ..models import Question, Answer, User, Tag

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

@router.get("/questions", response_model=List[Question])
async def search_questions(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("relevance", description="Sort by: relevance, newest, votes"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.search_questions(
        query=query,
        page=page,
        limit=limit,
        sort=sort or "relevance"
    )

@router.get("/answers", response_model=List[Answer])
async def search_answers(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("relevance", description="Sort by: relevance, newest, votes"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.search_answers(
        query=query,
        page=page,
        limit=limit,
        sort=sort or "relevance"
    )

@router.get("/users", response_model=List[User])
async def search_users(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("relevance", description="Sort by: relevance, reputation, newest"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.search_users(
        query=query,
        page=page,
        limit=limit,
        sort=sort or "relevance"
    )

@router.get("/tags", response_model=List[Tag])
async def search_tags(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("relevance", description="Sort by: relevance, popular, newest"),
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.search_tags(
        query=query,
        page=page,
        limit=limit,
        sort=sort or "relevance"
    )
