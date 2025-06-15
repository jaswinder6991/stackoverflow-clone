#!/usr/bin/env python3
"""
Test the voting system properly using the container API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_voting_system():
    print("🧪 Testing Container-based Voting System")
    print("=" * 50)
    
    # Create a fresh user for testing
    test_user = 12345
    question_id = 1
    
    # Get initial state
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code != 200:
        print("❌ Failed to get question")
        return
    
    initial_data = response.json()
    initial_votes = initial_data.get("votes", 0)
    print(f"Initial votes: {initial_votes}")
    
    # Test 1: Upvote
    print("\n1. Testing upvote...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user}&vote_type=up")
    if response.status_code == 200:
        print("✅ Upvote successful")
    else:
        print(f"❌ Upvote failed: {response.status_code}")
        return
    
    # Check result
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_upvote = response.json().get("votes", 0)
    expected_after_upvote = initial_votes + 1
    print(f"After upvote: {after_upvote} (expected: {expected_after_upvote})")
    
    if after_upvote == expected_after_upvote:
        print("✅ Upvote correctly applied")
    else:
        print("❌ Upvote not correctly applied")
    
    # Test 2: Duplicate upvote (should be prevented)
    print("\n2. Testing duplicate upvote prevention...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user}&vote_type=up")
    if response.status_code == 200:
        print("API call successful")
    
    # Check result
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_duplicate = response.json().get("votes", 0)
    print(f"After duplicate upvote: {after_duplicate} (should be same as before: {after_upvote})")
    
    if after_duplicate == after_upvote:
        print("✅ Duplicate upvote correctly prevented")
    else:
        print("❌ Duplicate upvote was not prevented")
    
    # Test 3: Change to downvote
    print("\n3. Testing vote change...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user}&vote_type=down")
    if response.status_code == 200:
        print("Vote change API call successful")
    
    # Check result
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_downvote = response.json().get("votes", 0)
    expected_after_downvote = initial_votes - 1  # Remove +1, add -1
    print(f"After downvote: {after_downvote} (expected: {expected_after_downvote})")
    
    if after_downvote == expected_after_downvote:
        print("✅ Vote change correctly applied")
    else:
        print("❌ Vote change not correctly applied")
    
    # Test 4: Duplicate downvote (should be prevented)
    print("\n4. Testing duplicate downvote prevention...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user}&vote_type=down")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_duplicate_down = response.json().get("votes", 0)
    
    if after_duplicate_down == after_downvote:
        print("✅ Duplicate downvote correctly prevented")
    else:
        print("❌ Duplicate downvote was not prevented")
    
    print("\n" + "=" * 50)
    print("🎉 Voting system test completed!")
    return True

if __name__ == "__main__":
    test_voting_system()
