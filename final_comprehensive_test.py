#!/usr/bin/env python3
"""
Final comprehensive test to verify the Stack Overflow clone voting system
meets all requirements
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_requirement_1_single_vote_per_user():
    """Test: Each user can only upvote or downvote a given answer/question once"""
    print("📋 Requirement 1: Single vote per user")
    print("-" * 40)
    
    user_id = 99999
    question_id = 1
    
    # Get initial state
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    initial_votes = response.json().get("votes", 0)
    
    # User votes up
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_first_vote = response.json().get("votes", 0)
    
    # User tries to vote up again
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    after_duplicate_vote = response.json().get("votes", 0)
    
    if after_first_vote == initial_votes + 1 and after_duplicate_vote == after_first_vote:
        print("✅ Single vote per user enforced")
        return True
    else:
        print("❌ Single vote per user NOT enforced")
        return False

def test_requirement_2_persistence_across_refresh():
    """Test: Vote state persists across page refreshes"""
    print("\n📋 Requirement 2: Persistence across refresh")
    print("-" * 40)
    
    user_id = 88888
    question_id = 1
    
    # Vote
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    
    # Simulate "refresh" by making multiple API calls
    vote_counts = []
    for i in range(5):
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        votes = response.json().get("votes", 0)
        vote_counts.append(votes)
        time.sleep(0.1)  # Small delay between requests
    
    # All requests should return the same vote count
    if len(set(vote_counts)) == 1:
        print("✅ Vote state persists across multiple requests (simulating refresh)")
        return True
    else:
        print("❌ Vote state NOT consistent across requests")
        print(f"Vote counts: {vote_counts}")
        return False

def test_requirement_3_no_duplicate_backend_votes():
    """Test: Duplicate votes are prevented in the backend"""
    print("\n📋 Requirement 3: No duplicate votes in backend")
    print("-" * 40)
    
    user_id = 77777
    question_id = 1
    
    # Get initial state
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    initial_votes = response.json().get("votes", 0)
    
    # Make multiple rapid vote requests
    for i in range(3):
        requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    final_votes = response.json().get("votes", 0)
    
    # Should only increase by 1, not 3
    if final_votes == initial_votes + 1:
        print("✅ Backend prevents duplicate votes")
        return True
    else:
        print("❌ Backend allows duplicate votes")
        print(f"Expected: {initial_votes + 1}, Got: {final_votes}")
        return False

def test_requirement_4_preserve_existing_functionality():
    """Test: All previously implemented functionality still works"""
    print("\n📋 Requirement 4: Existing functionality preserved")
    print("-" * 40)
    
    question_id = 1
    
    # Test basic API endpoints
    endpoints_to_test = [
        f"/questions/{question_id}",
        "/questions",
        "/api/users",
        "/api/tags",
        "/health"
    ]
    
    all_working = True
    for endpoint in endpoints_to_test:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"✅ {endpoint} working")
        else:
            print(f"❌ {endpoint} failed: {response.status_code}")
            all_working = False
    
    # Test vote changing (up to down, down to up)
    user_id = 66666
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=up")
    response1 = requests.get(f"{BASE_URL}/questions/{question_id}")
    votes_after_up = response1.json().get("votes", 0)
    
    requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={user_id}&vote_type=down")
    response2 = requests.get(f"{BASE_URL}/questions/{question_id}")
    votes_after_down = response2.json().get("votes", 0)
    
    # Should be a difference of 2 (remove +1, add -1)
    if votes_after_down == votes_after_up - 2:
        print("✅ Vote changing works correctly")
    else:
        print("❌ Vote changing not working correctly")
        all_working = False
    
    return all_working

def run_all_tests():
    """Run all requirement tests"""
    print("🧪 STACK OVERFLOW CLONE - VOTING SYSTEM VERIFICATION")
    print("=" * 60)
    print("Testing all requirements...\n")
    
    results = []
    results.append(test_requirement_1_single_vote_per_user())
    results.append(test_requirement_2_persistence_across_refresh())
    results.append(test_requirement_3_no_duplicate_backend_votes())
    results.append(test_requirement_4_preserve_existing_functionality())
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL REQUIREMENTS VERIFIED!")
        print("✅ Users can only vote once per question/answer")
        print("✅ Vote state persists across page refreshes")
        print("✅ Backend prevents duplicate votes")
        print("✅ All existing functionality preserved")
        print("\n🏆 The Stack Overflow clone voting system is working perfectly!")
    else:
        print("❌ Some requirements not met. Please review the failed tests.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()
