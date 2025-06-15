from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import questions, users, tags, search, answers, synthetic, auth, comments
from app.db.db import init_db, get_db, drop_db, populate_database
from app.db.models import User
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
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(comments.router)
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
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db = next(get_db())
    try:
        print("Ensuring database tables exist...")
        
        # First, always ensure tables are created/updated
        init_db()
        
        # Check if we need to recreate the database due to schema changes
        try:
            # Try to query the users table to see if it has the expected schema
            first_user = db.query(User).first()
            print("Database schema is compatible")
            
            if first_user is not None:
                print("Database already has data, skipping population")
                return
                
        except Exception as schema_error:
            print(f"Database schema mismatch detected: {schema_error}")
            print("Recreating database with updated schema...")
            db.close()
            
            # Drop and recreate the database
            drop_db()
            init_db()
            
            # Get a fresh database session
            db = next(get_db())

        print("Database is empty, populating with sample data...")
        try:
            # Populate with sample data
            populate_database(db)
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error during database population: {e}")
            raise
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)