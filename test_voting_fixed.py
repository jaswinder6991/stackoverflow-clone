#!/usr/bin/env python3
"""
Test script to verify the FIXED question voting behavior.
This will test the question voting endpoints with the new undo functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_fixed_question_voting():
    """Test fixed question voting behavior step by step"""
    
    # Step 1: Create a test question
    print("1. Creating a test question...")
    question_data = {
        "title": "Test Fixed Voting Question",
        "body": "This is a test question to verify FIXED voting behavior",
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
    
    # Step 4: Test removing upvote (toggle off with undo=true)
    print("\n4. Testing removing upvote (toggle off with undo=true)...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=up&undo=true")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Remove upvote successful. Response: {result}")
    else:
        print(f"Remove upvote failed: {response.status_code} - {response.text}")
    
    # Step 5: Get question state after removing upvote
    print("\n5. Getting question state after removing upvote...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Current vote count after removing upvote: {question['votes']}")
    
    # Step 6: Test downvote
    print("\n6. Testing downvote...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=down")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Downvote successful. Response: {result}")
    else:
        print(f"Downvote failed: {response.status_code} - {response.text}")
    
    # Step 7: Get question state after downvote
    print("\n7. Getting question state after downvote...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Current vote count after downvote: {question['votes']}")
    
    # Step 8: Test removing downvote (toggle off with undo=true)
    print("\n8. Testing removing downvote (toggle off with undo=true)...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id=1&vote_type=down&undo=true")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Remove downvote successful. Response: {result}")
    else:
        print(f"Remove downvote failed: {response.status_code} - {response.text}")
    
    # Step 9: Get final question state
    print("\n9. Getting final question state...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        question = response.json()
        print(f"Final vote count: {question['votes']}")
    
    print("\n" + "="*50)
    print("EXPECTED BEHAVIOR:")
    print("Initial: 0")
    print("After upvote: 1")
    print("After removing upvote: 0")
    print("After downvote: -1") 
    print("After removing downvote: 0")
    print("="*50)

if __name__ == "__main__":
    test_fixed_question_voting()
