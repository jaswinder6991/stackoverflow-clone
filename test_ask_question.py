#!/usr/bin/env python3

import requests
import json
import time
import random
import string

def random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def test_ask_question():
    """Test the ask question API endpoint"""
    print("Testing question creation...")
    
    # Generate random content for the question
    title = f"Test question {random_string()}"
    body = f"This is a test question body created at {time.time()}"
    tags = ["python", "test", "api"]
    
    # Create a question
    question_data = {
        "title": title,
        "body": body,
        "author_id": 1,  # Assuming user ID 1 exists
        "tags": tags  # Include the tags
    }
    
    # Send the request to create a question
    response = requests.post(
        "http://localhost:8000/questions/",
        json=question_data
    )
    
    # Check the response
    if response.status_code == 200:
        print("✓ Question created successfully")
        question = response.json()
        print(f"  ID: {question.get('id')}")
        print(f"  Title: {question.get('title')}")
        print(f"  Tags: {tags}")
        return question
    else:
        print(f"✗ Failed to create question: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

if __name__ == "__main__":
    test_ask_question()
