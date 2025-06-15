#!/usr/bin/env python3
"""
Comprehensive test script for the comment system
Tests all endpoints: create, fetch, vote, vote status
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_comment_system():
    print("🧪 Testing Comment System Functionality\n")
    
    # Test 1: Create comment on question
    print("1. Testing comment creation on question...")
    comment_data = {
        "body": "This is a test comment from the automated test suite. Great question about async/await!",
        "question_id": 1,
        "author_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/comments/", json=comment_data)
    if response.status_code == 200:
        comment = response.json()
        question_comment_id = comment['id']
        print(f"✅ Question comment created successfully with ID: {question_comment_id}")
    else:
        print(f"❌ Failed to create question comment: {response.text}")
        return
    
    # Test 2: Create comment on answer
    print("\n2. Testing comment creation on answer...")
    answer_comment_data = {
        "body": "This answer is very helpful but could use more specific examples of error handling patterns.",
        "answer_id": 1,
        "author_id": 2
    }
    
    response = requests.post(f"{BASE_URL}/comments/", json=answer_comment_data)
    if response.status_code == 200:
        comment = response.json()
        answer_comment_id = comment['id']
        print(f"✅ Answer comment created successfully with ID: {answer_comment_id}")
    else:
        print(f"❌ Failed to create answer comment: {response.text}")
        return
    
    # Test 3: Fetch question comments
    print("\n3. Testing question comment retrieval...")
    response = requests.get(f"{BASE_URL}/comments/question/1")
    if response.status_code == 200:
        comments = response.json()
        print(f"✅ Retrieved {len(comments)} comments for question 1")
        for comment in comments:
            print(f"   - Comment {comment['id']}: {comment['body'][:50]}... (votes: {comment['votes']})")
    else:
        print(f"❌ Failed to fetch question comments: {response.text}")
    
    # Test 4: Fetch answer comments
    print("\n4. Testing answer comment retrieval...")
    response = requests.get(f"{BASE_URL}/comments/answer/1")
    if response.status_code == 200:
        comments = response.json()
        print(f"✅ Retrieved {len(comments)} comments for answer 1")
        for comment in comments:
            print(f"   - Comment {comment['id']}: {comment['body'][:50]}... (votes: {comment['votes']})")
    else:
        print(f"❌ Failed to fetch answer comments: {response.text}")
    
    # Test 5: Vote on question comment
    print(f"\n5. Testing upvote on question comment {question_comment_id}...")
    response = requests.post(f"{BASE_URL}/comments/{question_comment_id}/vote", params={"user_id": 2})
    if response.status_code == 200:
        print("✅ Question comment upvoted successfully")
    else:
        print(f"❌ Failed to upvote question comment: {response.text}")
    
    # Test 6: Vote on answer comment
    print(f"\n6. Testing upvote on answer comment {answer_comment_id}...")
    response = requests.post(f"{BASE_URL}/comments/{answer_comment_id}/vote", params={"user_id": 1})
    if response.status_code == 200:
        print("✅ Answer comment upvoted successfully")
    else:
        print(f"❌ Failed to upvote answer comment: {response.text}")
    
    # Test 7: Check vote status
    print(f"\n7. Testing vote status check...")
    response = requests.get(f"{BASE_URL}/comments/{question_comment_id}/vote-status/2")
    if response.status_code == 200:
        vote_status = response.json()
        print(f"✅ Vote status retrieved: User 2 has_voted = {vote_status['has_voted']}")
    else:
        print(f"❌ Failed to check vote status: {response.text}")
    
    # Test 8: Verify vote counts increased
    print("\n8. Verifying vote counts increased...")
    response = requests.get(f"{BASE_URL}/comments/question/1")
    if response.status_code == 200:
        comments = response.json()
        for comment in comments:
            if comment['id'] == question_comment_id:
                if comment['votes'] > 0:
                    print(f"✅ Question comment {question_comment_id} now has {comment['votes']} vote(s)")
                else:
                    print(f"⚠️  Question comment {question_comment_id} still has {comment['votes']} votes")
    
    # Test 9: Toggle vote (remove vote)
    print(f"\n9. Testing vote toggle (removing vote)...")
    response = requests.post(f"{BASE_URL}/comments/{question_comment_id}/vote", params={"user_id": 2})
    if response.status_code == 200:
        print("✅ Vote toggled successfully")
        
        # Verify vote was removed
        time.sleep(0.5)  # Small delay
        response = requests.get(f"{BASE_URL}/comments/question/1")
        if response.status_code == 200:
            comments = response.json()
            for comment in comments:
                if comment['id'] == question_comment_id:
                    print(f"✅ After toggle, comment {question_comment_id} now has {comment['votes']} vote(s)")
                    break
    else:
        print(f"❌ Failed to toggle vote: {response.text}")
    
    print("\n🎉 Comment system testing completed!")

if __name__ == "__main__":
    test_comment_system()
