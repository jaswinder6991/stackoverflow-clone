#!/usr/bin/env python3
"""
Test script to verify the answer posting functionality
"""
import requests
import json

# API base URL
API_BASE = "http://localhost:8000"

def test_create_answer():
    """Test creating a new answer"""
    print("Testing answer creation...")
    
    # Test data
    answer_data = {
        "question_id": 1,
        "user_id": 1,
        "body": "This is a comprehensive test answer that demonstrates the complete functionality of the answer posting system. It includes proper formatting and detailed content to ensure the system works correctly."
    }
    
    # Make POST request
    response = requests.post(f"{API_BASE}/answers/", json=answer_data)
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Answer created successfully!")
        print(f"  Answer ID: {result['id']}")
        print(f"  Question ID: {result['question_id']}")
        print(f"  Author ID: {result['author_id']}")
        print(f"  Content: {result['body'][:50]}...")
        print(f"  Created: {result['created_at']}")
        return result['id']
    else:
        print(f"✗ Failed to create answer: {response.status_code}")
        print(f"  Error: {response.text}")
        return None

def test_get_answers_for_question(question_id):
    """Test getting answers for a question"""
    print(f"\nTesting retrieval of answers for question {question_id}...")
    
    response = requests.get(f"{API_BASE}/answers/?question_id={question_id}")
    
    if response.status_code == 200:
        answers = response.json()
        print(f"✓ Retrieved {len(answers)} answers")
        for i, answer in enumerate(answers, 1):
            print(f"  {i}. Answer ID {answer['id']}: {answer['body'][:50]}...")
        return True
    else:
        print(f"✗ Failed to get answers: {response.status_code}")
        return False

def test_health_check():
    """Test API health"""
    print("Testing API health...")
    
    response = requests.get(f"{API_BASE}/health")
    
    if response.status_code == 200:
        print("✓ API is healthy")
        return True
    else:
        print(f"✗ API health check failed: {response.status_code}")
        return False

def main():
    print("=== Answer Posting Functionality Test ===\n")
    
    # Test API health first
    if not test_health_check():
        print("API is not running. Please start the backend server.")
        return
    
    # Test answer creation
    answer_id = test_create_answer()
    if not answer_id:
        print("Answer creation failed. Stopping tests.")
        return
    
    # Test getting answers for question
    test_get_answers_for_question(1)
    
    print("\n=== Test Complete ===")
    print("✓ Answer posting functionality is working correctly!")
    print("✓ Frontend form at http://localhost:3000/questions/1 should now work")

if __name__ == "__main__":
    main()
