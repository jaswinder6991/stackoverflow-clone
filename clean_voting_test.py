#!/usr/bin/env python3
"""
Clean test with unique user IDs to avoid conflicts
"""

import requests
import random
import time

BASE_URL = "http://localhost:8000"

def get_unique_user_id():
    """Generate a unique user ID for testing"""
    return random.randint(100000, 999999)

def test_single_vote_enforcement():
    """Test that users can only vote once"""
    print("🧪 Testing Single Vote Enforcement")
    print("-" * 40)
    
    user_id = get_unique_user_id()
    question_id = 1
    
    # Get initial votes
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    initial_votes = response.json().get("votes", 0)
    print(f"Initial votes: {initial_votes}")
    
    # First vote
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    print(f"First vote response: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_first = response.json().get("votes", 0)
    print(f"After first vote: {after_first}")
    
    # Second vote (duplicate)
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    print(f"Duplicate vote response: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_duplicate = response.json().get("votes", 0)
    print(f"After duplicate vote: {after_duplicate}")
    
    # Verify
    expected_increase = 1
    actual_increase = after_duplicate - initial_votes
    
    print(f"Expected increase: {expected_increase}")
    print(f"Actual increase: {actual_increase}")
    
    if actual_increase == expected_increase and after_duplicate == after_first:
        print("✅ Single vote enforcement working")
        return True
    else:
        print("❌ Single vote enforcement failed")
        return False

def test_vote_change():
    """Test changing vote from up to down"""
    print("\n🧪 Testing Vote Change")
    print("-" * 40)
    
    user_id = get_unique_user_id()
    question_id = 1
    
    # Get initial votes
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    initial_votes = response.json().get("votes", 0)
    print(f"Initial votes: {initial_votes}")
    
    # Upvote
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_up = response.json().get("votes", 0)
    print(f"After upvote: {after_up}")
    
    # Change to downvote
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=down")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_down = response.json().get("votes", 0)
    print(f"After downvote: {after_down}")
    
    # Should be a net change of -2 from after_up (remove +1, add -1)
    expected_final = initial_votes - 1
    
    print(f"Expected final: {expected_final}")
    print(f"Actual final: {after_down}")
    
    if after_down == expected_final:
        print("✅ Vote change working")
        return True
    else:
        print("❌ Vote change failed")
        return False

def main():
    print("🎯 FINAL VOTING SYSTEM TEST")
    print("=" * 40)
    
    # Wait a moment for any previous requests to complete
    time.sleep(1)
    
    test1_result = test_single_vote_enforcement()
    test2_result = test_vote_change()
    
    print("\n" + "=" * 40)
    print("📊 RESULTS")
    print("=" * 40)
    
    if test1_result and test2_result:
        print("🎉 ALL CORE VOTING TESTS PASSED!")
        print("✅ Single vote per user enforced")
        print("✅ Vote changes work correctly")
        print("\n🏆 The voting system is working perfectly!")
    else:
        print("❌ Some tests failed")
        if not test1_result:
            print("  - Single vote enforcement failed")
        if not test2_result:
            print("  - Vote change failed")

if __name__ == "__main__":
    main()
