from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from .base import Base
from .models import User, Question, Answer, Tag, Vote, Badge, UserBadge, AnalyticsLog

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(data_dir, exist_ok=True)

# Database URL
db_path = os.path.join(data_dir, "sql_app.db")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
print(f"Using database at: {db_path}")

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Faker
fake = Faker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def drop_db():
    """Drop all tables in the database"""
    Base.metadata.drop_all(bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)

def is_database_empty(db):
    """Check if the database is empty by querying users table"""
    try:
        # Try to get the first user
        first_user = db.query(User).first()
        return first_user is None
    except Exception:
        # If there's an error (like table doesn't exist), consider it empty
        return True

def populate_database(db):
    """Populate the database with mock data only if it's empty"""
    if not is_database_empty(db):
        print("Database already has data, skipping population")
        return

    print("Database is empty, populating with sample data...")
    # Add sample users
    users = [
        User(
            name="john_doe",
            email="john@example.com",
            hashed_password="hashed_password",
            reputation=100,
            location="San Francisco, CA",
            website="https://johndoe.com",
            about="Full-stack developer passionate about Python and JavaScript",
            last_seen=datetime.utcnow(),
            profile={
                "basic": {
                    "displayName": "John Doe",
                    "location": "San Francisco, CA",
                    "title": "Senior Full Stack Developer",
                    "pronouns": "he/him",
                },
                "about": {
                    "bio": "Full-stack developer passionate about Python and JavaScript. I love building scalable web applications and contributing to open source projects.",
                    "interests": "Web Development, Cloud Computing, Open Source",
                },
                "developer": {
                    "primaryLanguage": "Python",
                    "technologies": "Python, JavaScript, React, Docker, AWS",
                    "yearsOfExperience": "8",
                    "githubProfile": "johndoe",
                },
                "links": {
                    "website": "https://johndoe.com",
                    "twitter": "@johndoe",
                    "github": "johndoe",
                }
            }
        ),
        User(
            name="jane_smith",
            email="jane@example.com",
            hashed_password="hashed_password",
            reputation=150,
            location="New York, NY",
            website="https://janesmith.dev",
            about="Senior software engineer specializing in React and TypeScript",
            last_seen=datetime.utcnow(),
            profile={
                "basic": {
                    "displayName": "Jane Smith",
                    "location": "New York, NY",
                    "title": "Senior Frontend Engineer",
                    "pronouns": "she/her",
                },
                "about": {
                    "bio": "Senior software engineer specializing in React and TypeScript. Currently focused on building performant and accessible web applications.",
                    "interests": "Frontend Development, UI/UX, Accessibility",
                },
                "developer": {
                    "primaryLanguage": "TypeScript",
                    "technologies": "React, TypeScript, Next.js, GraphQL",
                    "yearsOfExperience": "6",
                    "githubProfile": "janesmith",
                },
                "links": {
                    "website": "https://janesmith.dev",
                    "twitter": "@janesmith",
                    "github": "janesmith",
                }
            }
        ),
    ]
    db.add_all(users)
    
    # Add sample tags
    tags = [
        Tag(name="python", description="Python programming language"),
        Tag(name="javascript", description="JavaScript programming language"),
        Tag(name="react", description="React.js framework"),
    ]
    db.add_all(tags)
    
    # Add sample questions
    questions = [
        Question(
            title="How to use async/await in Python?",
            body="I'm trying to understand async/await in Python...",
            author=users[0],
            tags=[tags[0]]
        ),
        Question(
            title="React hooks best practices",
            body="What are the best practices for using React hooks?",
            author=users[1],
            tags=[tags[2]]
        ),
    ]
    db.add_all(questions)
    
    # Add sample answers
    answers = [
        Answer(
            body="Here's how you use async/await...",
            author=users[1],
            question=questions[0]
        ),
        Answer(
            body="For React hooks, you should...",
            author=users[0],
            question=questions[1]
        ),
    ]
    db.add_all(answers)
    
    # Add sample badges
    badges = [
        Badge(name="Nice Answer", description="Answer score of 10 or more", type="silver"),
        Badge(name="Good Question", description="Question score of 25 or more", type="silver"),
        Badge(name="Great Answer", description="Answer score of 100 or more", type="gold"),
    ]
    db.add_all(badges)
    
    # Add sample user badges
    user_badges = [
        UserBadge(user=users[0], badge=badges[0]),
        UserBadge(user=users[1], badge=badges[1]),
    ]
    db.add_all(user_badges)
    
    # Commit all changes
    db.commit()
    print("Database populated successfully!") 