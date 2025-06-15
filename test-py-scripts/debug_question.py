#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.data_service import DataService
from backend.app.db.db import get_db

# Test the data service directly
print("Testing DataService directly...")

try:
    # Get a database session
    db_gen = get_db()
    db = next(db_gen)
    
    # Create data service
    data_service = DataService(db)
    
    # Test get question by id
    print("Testing get_question_by_id...")
    question = data_service.get_question_by_id(2)
    print(f"Result: {question}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        db.close()
    except:
        pass
