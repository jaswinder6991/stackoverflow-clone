#!/usr/bin/env python3
"""
Test script to verify question voting behavior and identify the exact bug.
This will test the question voting endpoints directly to understand the backend behavior.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_question_voting():
    """Test question voting behavior step by step"""
    
    # Step 1: Create a test question
    print("1. Creating a test question...")
    question_data = {
        "title": "Test Voting Question",
        "body": "This is a test question to verify voting behavior",
        "author_id": 1,
        "tags": []
    }
    
    response = requests.post(f"{BASE_URL}/questions/", json=question_data)
    if response.status_code != 200:
        print(f"Failed to create question: {response.status_code} - {response.text}")
        return
    
    question = response.json()
    question_id = question["id"]
    print(f"Created question with ID: {question_id}")
    print(f"Initial vote count: {question['votes']}")
    
    # Step 2: Test upvote
    print("\n2. Testing upvote...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=up")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Upvote successful. Response: {result}")
    else:
        print(f"Upvote failed: {response.status_code} - {response.text}")
        
    # Step 3: Get current question state
    print("\n3. Getting current question state...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Current vote count: {question['votes']}")
    
    # Step 4: Test downvote (should change from up to down)
    print("\n4. Testing downvote (changing from up to down)...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=down")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Downvote successful. Response: {result}")
    else:
        print(f"Downvote failed: {response.status_code} - {response.text}")
    
    # Step 5: Get current question state after downvote
    print("\n5. Getting question state after downvote...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Current vote count after downvote: {question['votes']}")
    
    # Step 6: Test removing downvote (toggle off)
    print("\n6. Testing removing downvote (toggle off)...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=down")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Remove downvote successful. Response: {result}")
    else:
        print(f"Remove downvote failed: {response.status_code} - {response.text}")
    
    # Step 7: Get final question state
    print("\n7. Getting final question state...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Final vote count: {question['votes']}")
    
    print("\n" + "="*50)
    print("EXPECTED BEHAVIOR:")
    print("Initial: 0")
    print("After upvote: 1")
    print("After changing to downvote: -1 (remove +1, add -1)")
    print("After removing downvote: 0 (remove -1)")

if __name__ == "__main__":
    test_question_voting()
