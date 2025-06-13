from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import questions, users, tags, search, answers, synthetic, auth
from app.db.db import init_db, get_db, drop_db, populate_database
from sqlalchemy.orm import Session

app = FastAPI(
    title="Stack Overflow Clone API",
    description="A FastAPI backend for the Stack Overflow clone Next.js application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(users.router)
app.include_router(tags.router)
app.include_router(search.router)
app.include_router(synthetic.router)

@app.get("/")
async def root():
    return {
        "message": "Stack Overflow Clone API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint that verifies database connectivity"""
    try:
        # Try to make a simple database query
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    # Drop existing tables
    drop_db()
    # Create tables with new schema
    init_db()
    # Populate with sample data
    db = next(get_db())
    try:
        populate_database(db)
    except Exception as e:
        print(f"Error populating database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
