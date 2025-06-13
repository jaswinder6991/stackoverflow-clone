from fastapi import APIRouter, HTTPException, Request, Response, Cookie, Depends
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import json
from ..db.db import get_db, populate_database
from ..db.models import AnalyticsLog
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

router = APIRouter(prefix="/_synthetic", tags=["synthetic"])

# In-memory storage for sessions
sessions: Dict[str, Dict[str, Any]] = {}

@router.post("/new_session")
async def new_session(seed: Optional[int] = None, response: Response = None):
    """Create a new session with optional seed for reproducible data"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "created_at": datetime.utcnow(),
        "seed": seed
    }
    
    # Set session cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )
    
    return {"session_id": session_id}

@router.post("/log_event")
async def log_event(
    request: Request,
    event: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Log a custom event"""
    try:
        # Get or create session ID
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            response = Response()
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=3600,
                samesite="lax"
            )
        
        # Create analytics log
        log = AnalyticsLog(
            session_id=session_id,
            event_type=event.get("type", "CUSTOM"),
            event_data=json.dumps(event),
            timestamp=datetime.utcnow()
        )
        
        # Save to database
        db.add(log)
        db.commit()
        
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_logs(
    session_id: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """Get logs for a session"""
    if not session_id:
        raise HTTPException(status_code=400, detail="No session ID provided")
    
    logs = db.query(AnalyticsLog).filter(
        AnalyticsLog.session_id == session_id
    ).order_by(AnalyticsLog.created_at.desc()).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "action_type": log.action_type,
                "page_url": log.page_url,
                "payload": log.payload,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
    }

@router.post("/reset")
async def reset_environment(
    seed: Optional[int] = None,
    session_id: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """Reset the environment and optionally reseed"""
    if session_id:
        sessions[session_id] = {
            "created_at": datetime.utcnow(),
            "seed": seed
        }
    
    # Reset database with new seed
    populate_database(db, seed)
    
    return {"status": "ok", "seed": seed}

@router.get("/populate")
async def populate_db(db: Session = Depends(get_db)):
    """Populate database with sample data"""
    try:
        populate_database(db)
        return {"status": "success", "message": "Database populated with sample data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 