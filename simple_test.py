#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:8000"

# Create question
resp = requests.post(f"{BASE_URL}/questions/", json={
    "title": "Simple Test", "body": "Simple test", "author_id": 1, "tags": []
})
qid = resp.json()["id"]
print(f"Question {qid} created")

def get_votes():
    return requests.get(f"{BASE_URL}/questions/{qid}").json()["votes"]

# Test sequence
print(f"Initial: {get_votes()}")

requests.post(f"{BASE_URL}/questions/{qid}/vote?user_id=1&vote_type=up")
print(f"After upvote: {get_votes()}")

requests.post(f"{BASE_URL}/questions/{qid}/vote?user_id=1&vote_type=up&undo=true")
print(f"After removing upvote: {get_votes()}")

requests.post(f"{BASE_URL}/questions/{qid}/vote?user_id=1&vote_type=down")
print(f"After downvote: {get_votes()}")

requests.post(f"{BASE_URL}/questions/{qid}/vote?user_id=1&vote_type=down&undo=true")
print(f"After removing downvote: {get_votes()}")
