#!/usr/bin/env python3
"""
Final Answer Posting Verification Test
Simple test to verify end-to-end answer posting functionality
"""

import requests
import json
from datetime import datetime

def test_answer_posting():
    print("🚀 Final Answer Posting Test")
    print("=" * 40)
    
    # Test 1: Check backend health
    print("1. Checking backend health...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("   ✅ Backend is healthy")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return False
    
    # Test 2: Get a question to test with
    print("2. Getting test question...")
    try:
        response = requests.get("http://localhost:8000/questions/")
        if response.status_code == 200:
            data = response.json()
            questions = data.get('items', [])
            if questions:
                test_question = questions[0]
                question_id = test_question['id']
                print(f"   ✅ Testing with question ID {question_id}: '{test_question['title']}'")
            else:
                print("   ❌ No questions found")
                return False
        else:
            print(f"   ❌ Failed to get questions: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting questions: {e}")
        return False
    
    # Test 3: Get current answer count
    print("3. Getting current answers...")
    try:
        response = requests.get(f"http://localhost:8000/questions/{question_id}/answers")
        if response.status_code == 200:
            initial_answers = response.json()
            initial_count = len(initial_answers)
            print(f"   ✅ Question currently has {initial_count} answers")
        else:
            print(f"   ❌ Failed to get answers: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting answers: {e}")
        return False
    
    # Test 4: Create a new answer
    print("4. Creating new answer...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answer_body = f"""
This is a test answer created at {timestamp} to verify the end-to-end answer posting functionality.

✅ Backend API is working
✅ Database persistence is working  
✅ Answer creation endpoint is functional

The Stack Overflow clone's answer posting feature is now fully operational!
"""
    
    answer_data = {
        "question_id": question_id,
        "user_id": 1,
        "body": answer_body
    }
    
    try:
        response = requests.post("http://localhost:8000/answers/", json=answer_data)
        if response.status_code == 200:
            new_answer = response.json()
            print(f"   ✅ Created answer ID {new_answer['id']}")
        else:
            print(f"   ❌ Failed to create answer: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error creating answer: {e}")
        return False
    
    # Test 5: Verify answer was added
    print("5. Verifying answer was added...")
    try:
        response = requests.get(f"http://localhost:8000/questions/{question_id}/answers")
        if response.status_code == 200:
            final_answers = response.json()
            final_count = len(final_answers)
            if final_count > initial_count:
                print(f"   ✅ Answer count increased from {initial_count} to {final_count}")
                print(f"   ✅ New answer is visible in the API")
            else:
                print(f"   ❌ Answer count didn't increase ({initial_count} -> {final_count})")
                return False
        else:
            print(f"   ❌ Failed to verify answers: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error verifying answers: {e}")
        return False
    
    # Success summary
    print("\n🎉 SUCCESS!")
    print(f"✅ Answer posting functionality is working correctly")
    print(f"✅ Question ID {question_id} now has {final_count} answers")
    print(f"✅ New answer ID: {new_answer['id']}")
    print(f"🌐 View at: http://localhost:3000/questions/{question_id}")
    
    return True

if __name__ == "__main__":
    success = test_answer_posting()
    if not success:
        print("\n❌ Test failed!")
        exit(1)
    else:
        print("\n✅ All tests passed!")
