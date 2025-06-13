from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import List, Dict, Any

app = FastAPI(
    title="Stack Overflow Clone API",
    description="A FastAPI backend for the Stack Overflow clone Next.js application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
def load_data():
    data = {}
    try:
        with open("data/users.json", "r") as f:
            data["users"] = json.load(f)
        with open("data/questions.json", "r") as f:
            data["questions"] = json.load(f)
        with open("data/answers.json", "r") as f:
            data["answers"] = json.load(f)
        with open("data/tags.json", "r") as f:
            data["tags"] = json.load(f)
        print(f"Loaded {len(data['users'])} users, {len(data['questions'])} questions, {len(data['answers'])} answers, {len(data['tags'])} tags")
    except FileNotFoundError as e:
        print(f"Data file not found: {e}")
        data = {"users": [], "questions": [], "answers": [], "tags": []}
    return data

# Global data
data = load_data()

@app.get("/")
async def root():
    return {
        "message": "Stack Overflow Clone API",
        "version": "1.0.0",
        "docs": "/docs",
        "data_loaded": {
            "users": len(data["users"]),
            "questions": len(data["questions"]),
            "answers": len(data["answers"]),
            "tags": len(data["tags"])
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "data_loaded": len(data["users"]) > 0}

# Questions endpoints
@app.get("/api/questions/")
async def get_questions(skip: int = 0, limit: int = 15):
    """Get paginated list of questions"""
    questions = data["questions"].copy()
    
    # Add answer count to each question
    for question in questions:
        question["answer_count"] = len([ans for ans in data["answers"] if ans["question_id"] == question["id"]])
    
    # Sort by newest (highest ID)
    questions.sort(key=lambda x: x["id"], reverse=True)
    
    return questions[skip:skip + limit]

@app.get("/api/questions/{question_id}")
async def get_question(question_id: int):
    """Get a specific question with its answers"""
    question = next((q for q in data["questions"] if q["id"] == question_id), None)
    
    if not question:
        return {"error": "Question not found"}, 404
    
    # Add answers to question
    question_answers = [ans for ans in data["answers"] if ans["question_id"] == question_id]
    question["answers"] = question_answers
    
    # Increment view count
    question["views"] = question.get("views", 0) + 1
    
    return question

# Users endpoints
@app.get("/api/users/")
async def get_users(skip: int = 0, limit: int = 20):
    """Get paginated list of users"""
    return data["users"][skip:skip + limit]

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user"""
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    
    if not user:
        return {"error": "User not found"}, 404
    
    return user

# Tags endpoints
@app.get("/api/tags/")
async def get_tags(skip: int = 0, limit: int = 20):
    """Get paginated list of tags"""
    # Sort by popularity (count)
    tags = sorted(data["tags"], key=lambda x: x["count"], reverse=True)
    return tags[skip:skip + limit]

@app.get("/api/tags/{tag_name}")
async def get_tag(tag_name: str):
    """Get a specific tag"""
    tag = next((t for t in data["tags"] if t["name"].lower() == tag_name.lower()), None)
    
    if not tag:
        return {"error": "Tag not found"}, 404
    
    return tag

# Answers endpoints
@app.get("/api/answers/question/{question_id}")
async def get_answers_by_question(question_id: int):
    """Get all answers for a specific question"""
    answers = [ans for ans in data["answers"] if ans["question_id"] == question_id]
    return answers

@app.get("/api/answers/{answer_id}")
async def get_answer(answer_id: int):
    """Get a specific answer"""
    answer = next((a for a in data["answers"] if a["id"] == answer_id), None)
    
    if not answer:
        return {"error": "Answer not found"}, 404
    
    return answer

# Search endpoints
@app.get("/api/search/")
async def search_all(q: str, skip: int = 0, limit: int = 15):
    """Search across questions, users, and tags"""
    results = {
        "query": q,
        "questions": [],
        "users": [],
        "tags": []
    }
    
    # Search questions
    for question in data["questions"]:
        if q.lower() in question["title"].lower() or q.lower() in question["content"].lower():
            question["answer_count"] = len([ans for ans in data["answers"] if ans["question_id"] == question["id"]])
            results["questions"].append(question)
    
    # Search users
    for user in data["users"]:
        if q.lower() in user["name"].lower() or q.lower() in user.get("location", "").lower():
            results["users"].append(user)
    
    # Search tags
    for tag in data["tags"]:
        if q.lower() in tag["name"].lower() or q.lower() in tag.get("description", "").lower():
            results["tags"].append(tag)
    
    # Limit results
    results["questions"] = results["questions"][skip:skip + limit]
    results["users"] = results["users"][skip:skip + limit]
    results["tags"] = results["tags"][skip:skip + limit]
    
    return results

# Mock POST endpoints
@app.post("/api/questions/")
async def create_question(question: dict):
    """Create a new question (mock)"""
    return {"message": f"Question '{question.get('title')}' would be created", "success": True}

@app.post("/api/answers/")
async def create_answer(answer: dict):
    """Create a new answer (mock)"""
    return {"message": f"Answer would be created for question {answer.get('question_id')}", "success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# Create app instance for uvicorn
application = app
