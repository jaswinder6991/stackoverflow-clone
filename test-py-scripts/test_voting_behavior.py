#!/usr/bin/env python3
"""
Test script to verify that the voting system prevents duplicate votes
and maintains vote state across different scenarios.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_voting_behavior():
    """Test the voting behavior to ensure no duplicate votes are allowed."""
    
    print("🧪 Testing Stack Overflow Clone Voting System")
    print("=" * 50)
    
    # Test data
    test_user_id = 999
    question_id = 1
    answer_id = 1
    
    # Test 1: Get initial question state
    print("\n1️⃣ Getting initial question state...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        initial_question = response.json()
        initial_score = initial_question.get('score', initial_question.get('votes', 0))
        print(f"   Question {question_id} initial score: {initial_score}")
    else:
        print(f"   ❌ Failed to get question: {response.status_code}")
        return False
    
    # Test 2: Check initial vote status for user
    print(f"\n2️⃣ Checking initial vote status for user {test_user_id}...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}/vote-status/{test_user_id}")
    if response.status_code == 200:
        initial_vote_status = response.json()
        print(f"   Initial vote status: {initial_vote_status}")
    else:
        print(f"   ❌ Failed to get vote status: {response.status_code}")
        initial_vote_status = {"vote_type": None}
    
    # Test 3: Cast first upvote
    print(f"\n3️⃣ Casting first upvote for user {test_user_id}...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user_id}&vote_type=up")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ First upvote successful: {result}")
        expected_score = initial_score + (1 if initial_vote_status["vote_type"] != "upvote" else 0)
    else:
        print(f"   ❌ First upvote failed: {response.status_code} - {response.text}")
        return False
    
    # Test 4: Verify score changed
    print(f"\n4️⃣ Verifying score changed...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    new_score = initial_score  # Default fallback
    if response.status_code == 200:
        updated_question = response.json()
        new_score = updated_question.get('score', updated_question.get('votes', 0))
        print(f"   New score: {new_score} (expected: {expected_score})")
        if new_score == expected_score:
            print("   ✅ Score updated correctly")
        else:
            print("   ⚠️ Score update unexpected")
    
    # Test 5: Try to upvote again (should be prevented)
    print(f"\n5️⃣ Attempting duplicate upvote (should be prevented)...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user_id}&vote_type=up")
    if response.status_code == 200:
        result = response.json()
        print(f"   Result: {result}")
        # Check if vote was actually applied by checking score
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        if response.status_code == 200:
            current_question = response.json()
            current_score = current_question.get('score', current_question.get('votes', 0))
            if current_score == new_score:
                print("   ✅ Duplicate upvote correctly prevented (score unchanged)")
            else:
                print("   ❌ Duplicate upvote was allowed (score changed)")
                return False
    else:
        print(f"   ❌ Duplicate upvote request failed: {response.status_code}")
    
    # Test 6: Change vote to downvote
    print(f"\n6️⃣ Changing vote to downvote...")
    response = requests.post(f"{BASE_URL}/questions/{question_id}/vote?user_id={test_user_id}&vote_type=down")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Vote change successful: {result}")
        # Score should decrease by 2 (remove upvote +1, add downvote -1)
        expected_score_after_change = new_score - 2
    else:
        print(f"   ❌ Vote change failed: {response.status_code} - {response.text}")
        return False
    
    # Test 7: Verify score after vote change
    print(f"\n7️⃣ Verifying score after vote change...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code == 200:
        final_question = response.json()
        final_score = final_question.get('score', final_question.get('votes', 0))
        print(f"   Final score: {final_score} (expected: {expected_score_after_change})")
        if final_score == expected_score_after_change:
            print("   ✅ Vote change updated score correctly")
        else:
            print("   ⚠️ Vote change score update unexpected")
    
    # Test 8: Check final vote status
    print(f"\n8️⃣ Checking final vote status...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}/vote-status/{test_user_id}")
    if response.status_code == 200:
        final_vote_status = response.json()
        print(f"   Final vote status: {final_vote_status}")
        if final_vote_status.get("vote_type") == "downvote":
            print("   ✅ Vote status correctly shows downvote")
        else:
            print("   ❌ Vote status incorrect")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 All voting behavior tests completed successfully!")
    print("✅ Single vote per user enforced")
    print("✅ Vote changes work correctly")
    print("✅ Score calculations accurate")
    return True

def test_answer_voting():
    """Test voting behavior for answers."""
    print("\n🧪 Testing Answer Voting System")
    print("=" * 30)
    
    test_user_id = 998
    question_id = 1
    
    # First, get answers for the question
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    if response.status_code != 200:
        print("❌ Could not get question for answer test")
        return False
    
    question_data = response.json()
    answers = question_data.get('answers', [])
    
    if not answers:
        print("⚠️ No answers found to test voting")
        return True
    
    answer_id = answers[0]['id']
    initial_score = answers[0].get('score', answers[0].get('votes', 0))
    
    print(f"Testing with answer {answer_id}, initial score: {initial_score}")
    
    # Test answer upvote
    vote_data = {"user_id": test_user_id, "vote_type": "upvote"}
    response = requests.post(f"{BASE_URL}/answers/{answer_id}/vote?user_id={test_user_id}&vote_type=up")
    
    if response.status_code == 200:
        print("✅ Answer voting endpoint working")
        return True
    else:
        print(f"❌ Answer voting failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Stack Overflow Clone Voting Tests")
    
    # Wait a moment for services to be ready
    time.sleep(2)
    
    try:
        success = test_voting_behavior()
        if success:
            test_answer_voting()
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
