from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .routers import auth, users, questions, answers, tags, search, synthetic
from .db.db import init_db, drop_db, get_db, populate_database
import secrets

app = FastAPI()

# Generate a secure secret key
SECRET_KEY = secrets.token_urlsafe(32)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session_id",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=False  # Set to True in production
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Drop existing tables
        drop_db()
        # Create tables with new schema
        init_db()
        # Populate with sample data
        db = next(get_db())
        try:
            populate_database(db)
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error populating database: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(tags.router)
app.include_router(search.router)
app.include_router(synthetic.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"} 