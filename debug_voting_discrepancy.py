#!/usr/bin/env python3
"""
Direct test of database vs API response to identify the discrepancy
"""

import requests
import json
from sqlalchemy.orm import Session
from backend.app.db.db import engine
from backend.app.db.models import Question, Vote

def test_direct_db_access():
    """Test direct database access"""
    print("🔍 Testing Direct Database Access")
    print("=" * 40)
    
    db = Session(bind=engine)
    
    # Get question directly from database
    question = db.query(Question).filter(Question.id == 1).first()
    if question:
        print(f"Database Question ID: {question.id}")
        print(f"Database Question Votes: {question.votes}")
        print(f"Database Question Views: {question.views}")
    
    # Get votes for this question
    votes = db.query(Vote).filter(Vote.question_id == 1).all()
    print(f"Votes for Question 1: {len(votes)}")
    for vote in votes:
        print(f"  User {vote.user_id}: {vote.vote_type}")
    
    db.close()

def test_api_response():
    """Test API response"""
    print("\n🌐 Testing API Response")
    print("=" * 40)
    
    response = requests.get("http://localhost:8000/questions/1")
    if response.status_code == 200:
        data = response.json()
        print(f"API Question ID: {data.get('id')}")
        print(f"API Question Votes: {data.get('votes')}")
        print(f"API Question Views: {data.get('views')}")
        print(f"API Question Score: {data.get('score')}")
    else:
        print(f"API Error: {response.status_code}")

def test_vote_api():
    """Test voting through API"""
    print("\n🗳️ Testing Vote API")
    print("=" * 40)
    
    # Vote through API
    response = requests.post("http://localhost:8000/questions/1/vote?user_id=777&vote_type=up")
    print(f"Vote API Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Vote Response: {response.json()}")
    
    # Check result
    response = requests.get("http://localhost:8000/questions/1")
    if response.status_code == 200:
        data = response.json()
        print(f"After Vote - API Votes: {data.get('votes')}")

if __name__ == "__main__":
    test_direct_db_access()
    test_api_response()
    test_vote_api()
    test_direct_db_access()  # Check again after API vote
