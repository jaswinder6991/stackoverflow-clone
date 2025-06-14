#!/usr/bin/env python3
"""
Test the frontend API service functionality
"""
import requests
import json

def test_frontend_api_simulation():
    """Simulate what the frontend AnswerForm should be doing"""
    print("🧪 Testing Frontend API Service Simulation")
    print("=" * 50)
    
    # Test 1: Health check (like the frontend would do)
    print("\n1. Testing health check...")
    try:
        response = requests.get('http://localhost:8000/health')
        print(f"✓ Health Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test 2: Test answer posting to question 2 (the problematic one)
    print("\n2. Testing answer posting to question 2...")
    answer_data = {
        'question_id': 2,
        'user_id': 1,
        'body': 'This is a test answer submitted via the simulated frontend API call to question 2. This should work exactly like the frontend AnswerForm component.'
    }
    
    try:
        response = requests.post('http://localhost:8000/answers/', json=answer_data)
        print(f"✓ Answer Post Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Answer ID: {result['id']}")
            print(f"  Question ID: {result['question_id']}")
            print(f"  Content: {result['body'][:60]}...")
        else:
            print(f"✗ Error response: {response.text}")
    except Exception as e:
        print(f"✗ Answer posting failed: {e}")
    
    # Test 3: Test answer posting to question 4 (the new one we created)
    print("\n3. Testing answer posting to question 4...")
    answer_data = {
        'question_id': 4,
        'user_id': 1,
        'body': 'This is a test answer submitted via the simulated frontend API call to question 4 (the newly created question). The frontend form should work identically to this.'
    }
    
    try:
        response = requests.post('http://localhost:8000/answers/', json=answer_data)
        print(f"✓ Answer Post Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Answer ID: {result['id']}")
            print(f"  Question ID: {result['question_id']}")
            print(f"  Content: {result['body'][:60]}...")
        else:
            print(f"✗ Error response: {response.text}")
    except Exception as e:
        print(f"✗ Answer posting failed: {e}")
    
    # Test 4: Get answers for a question to verify they were stored
    print("\n4. Retrieving answers for question 2...")
    try:
        response = requests.get('http://localhost:8000/answers/?question_id=2')
        print(f"✓ Get Answers Status: {response.status_code}")
        if response.status_code == 200:
            answers = response.json()
            print(f"  Found {len(answers)} answers for question 2")
            for i, answer in enumerate(answers[-2:], 1):  # Show last 2 answers
                print(f"    {i}. Answer {answer['id']}: {answer['body'][:40]}...")
        else:
            print(f"✗ Error getting answers: {response.text}")
    except Exception as e:
        print(f"✗ Getting answers failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 CONCLUSION:")
    print("If all tests above passed, the API is working correctly.")
    print("Any frontend issues are likely in the React component or API service.")
    print("Check browser console for JavaScript errors when testing the actual frontend.")

if __name__ == "__main__":
    test_frontend_api_simulation()
