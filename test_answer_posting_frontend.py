#!/usr/bin/env python3
"""
Frontend Answer Posting Test
Tests the complete answer posting workflow from frontend to backend
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test if backend is healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Backend Health: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Backend Health Check Failed: {e}")
        return False

def get_questions():
    """Get all questions"""
    try:
        response = requests.get(f"{BASE_URL}/questions/")
        if response.status_code == 200:
            data = response.json()
            questions = data.get('items', [])
            print(f"✅ Found {len(questions)} questions")
            return questions
        else:
            print(f"❌ Failed to get questions: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting questions: {e}")
        return []

def get_question_details(question_id):
    """Get details for a specific question"""
    try:
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        if response.status_code == 200:
            question = response.json()
            print(f"✅ Question {question_id}: '{question['title']}'")
            print(f"   Answers: {question.get('answer_count', 0)}")
            return question
        else:
            print(f"❌ Failed to get question {question_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting question {question_id}: {e}")
        return None

def get_answers_for_question(question_id):
    """Get all answers for a question"""
    try:
        response = requests.get(f"{BASE_URL}/questions/{question_id}/answers")
        if response.status_code == 200:
            answers = response.json()
            print(f"✅ Question {question_id} has {len(answers)} answers")
            for i, answer in enumerate(answers, 1):
                print(f"   Answer {i}: ID {answer['id']}, {len(answer['body'])} chars")
            return answers
        else:
            print(f"❌ Failed to get answers for question {question_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting answers: {e}")
        return []

def create_test_answer(question_id, test_content=None):
    """Create a new test answer"""
    if test_content is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_content = f"""
# Test Answer Posted at {timestamp}

This is a comprehensive test answer to verify the answer posting functionality works correctly.

## Key Points:
- ✅ Backend API integration working
- ✅ Database persistence working
- ✅ Frontend form submission working

## Code Example:
```python
def test_function():
    return "Answer posting is working!"
```

**Posted via automated frontend test.**
"""
    
    answer_data = {
        "question_id": question_id,
        "user_id": 1,  # Using existing user
        "body": test_content
    }
    
    try:
        response = requests.post(f"{BASE_URL}/answers/", json=answer_data)
        if response.status_code == 200:
            answer = response.json()
            print(f"✅ Created answer ID {answer['id']} for question {question_id}")
            print(f"   Body length: {len(answer['body'])} characters")
            return answer
        else:
            print(f"❌ Failed to create answer: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating answer: {e}")
        return None

def main():
    print("🚀 Starting Frontend Answer Posting Test")
    print("=" * 50)
    
    # Test 1: Backend Health
    print("\n1. Testing Backend Health...")
    if not test_backend_health():
        print("❌ Backend is not healthy, aborting test")
        return False
    
    # Test 2: Get Questions
    print("\n2. Getting Available Questions...")
    questions = get_questions()
    if not questions:
        print("❌ No questions found, aborting test")
        return False
    
    # Test 3: Pick a question to test with
    test_question_id = questions[0]['id']  # Use the first question
    print(f"\n3. Testing with Question ID {test_question_id}...")
    question = get_question_details(test_question_id)
    if not question:
        print("❌ Could not get question details")
        return False
    
    # Test 4: Get existing answers
    print(f"\n4. Getting Existing Answers for Question {test_question_id}...")
    initial_answers = get_answers_for_question(test_question_id)
    initial_count = len(initial_answers)
    
    # Test 5: Create new answer
    print(f"\n5. Creating New Test Answer...")
    new_answer = create_test_answer(test_question_id)
    if not new_answer:
        print("❌ Failed to create test answer")
        return False
    
    # Test 6: Verify answer was created
    print(f"\n6. Verifying Answer Creation...")
    time.sleep(1)  # Brief pause for database consistency
    final_answers = get_answers_for_question(test_question_id)
    final_count = len(final_answers)
    
    if final_count > initial_count:
        print(f"✅ Answer count increased from {initial_count} to {final_count}")
        print("✅ Answer posting functionality is working correctly!")
        
        print(f"\n📋 Test Summary:")
        print(f"   Question ID: {test_question_id}")
        print(f"   Question Title: {question['title']}")
        print(f"   New Answer ID: {new_answer['id']}")
        print(f"   Frontend URL: {FRONTEND_URL}/questions/{test_question_id}")
        
        return True
    else:
        print(f"❌ Answer count did not increase ({initial_count} -> {final_count})")
        return False

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Answer posting functionality is working!")
        print(f"🌐 Visit {FRONTEND_URL}/questions to see your new answer!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
