#!/usr/bin/env python3
"""
Initialize the database with tables and sample data
"""
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, init_db, populate_database

def main():
    print("Initializing database...")
    
    # Create all tables
    init_db()
    print("✓ Tables created")
    
    # Create session and populate with sample data
    db = SessionLocal()
    try:
        populate_database(db)
        print("✓ Sample data populated")
    except Exception as e:
        print(f"Error populating data: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    main()
