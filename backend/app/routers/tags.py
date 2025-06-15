from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db.db import get_db
from ..data_service import DataService
from ..models import Tag, PaginatedResponse, TagCreate, TagUpdate

router = APIRouter(prefix="/api/tags", tags=["tags"])

@router.get("/", response_model=PaginatedResponse[Tag])
async def get_tags(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search tags by name or description"),
    sort: Optional[str] = Query("popular", description="Sort by: popular, name, newest"),
    db: Session = Depends(get_db)
):
    """Get a paginated list of tags with optional search and sorting"""
    data_service = DataService(db)
    tags = data_service.get_tags(page=page, limit=limit, search=search, sort=sort or "popular")
    return tags

@router.get("/{tag_name}", response_model=Tag)
async def get_tag(
    tag_name: str,
    db: Session = Depends(get_db)
):
    """Get a specific tag by name"""
    data_service = DataService(db)
    tag = data_service.get_tag_by_name(tag_name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/{tag_name}/questions", response_model=PaginatedResponse)
async def get_tag_questions(
    tag_name: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Optional[str] = Query("newest", description="Sort by: newest, votes, activity"),
    db: Session = Depends(get_db)
):
    """Get questions tagged with a specific tag"""
    # Check if tag exists
    data_service = DataService(db)
    tag = data_service.get_tag_by_name(tag_name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    questions = data_service.get_questions_by_tag(tag_name, page=page, limit=limit, sort=sort or "newest")
    return questions

@router.get("/stats/popular")
async def get_popular_tags(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get most popular tags"""
    data_service = DataService(db)
    tags = data_service.get_popular_tags(limit=limit)
    return {"tags": tags}

@router.get("/stats/trending")
async def get_trending_tags(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get trending tags (most activity in recent period)"""
    data_service = DataService(db)
    tags = data_service.get_trending_tags(limit=limit)
    return {"tags": tags}

@router.post("/", response_model=Tag)
async def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    return data_service.create_tag(tag)

@router.put("/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    tag = data_service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Update tag fields
    for field, value in tag_update.dict(exclude_unset=True).items():
        setattr(tag, field, value)
    
    db.commit()
    db.refresh(tag)
    return tag

@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    data_service = DataService(db)
    tag = data_service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
