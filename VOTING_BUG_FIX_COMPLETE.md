# Question Voting Bug Fix - Complete

## Problem Description
The question upvote/downvote mechanism had a critical bug where:
- Clicking downvote would increment the count instead of decrementing it
- Toggling votes (clicking the same button twice) would not return the count to its former value
- The UI changes were not persistent after refresh

## Root Cause Analysis
The issue was caused by a **double bug**:

1. **Backend Issue**: The backend voting logic (`vote_question` in `data_service.py`) did not support vote removal (toggle-off functionality). When a user clicked the same vote button twice, the backend would simply return early with no changes instead of removing the vote.

2. **Frontend Workaround Gone Wrong**: The frontend (`api.ts`) had a buggy workaround that tried to "cancel out" votes by sending the opposite vote type when `isUndo=true`. This caused:
   - Upvote toggle → Send downvote → Backend treats as vote change → Wrong count
   - User confusion and incorrect vote tallies

## Solution Implemented

### Backend Changes

1. **Added `undo` parameter to voting endpoints**:
   - `POST /questions/{question_id}/vote?undo=true`
   - `POST /answers/{answer_id}/vote?undo=true`

2. **Added vote removal methods**:
   - `remove_question_vote()` in `DataService`
   - `remove_answer_vote()` in `DataService`

3. **Updated routing logic**:
   - When `undo=true`, calls removal methods
   - When `undo=false` (default), calls existing voting methods

### Frontend Changes

1. **Fixed API service methods**:
   - Removed buggy opposite-vote-type workaround
   - Now properly sends `undo=true` parameter to backend
   - Maintains correct `voteType` when undoing

2. **Preserved existing UI logic**:
   - Frontend voting logic in `QuestionDetail.tsx` unchanged
   - Optimistic updates still work correctly
   - Vote state tracking remains the same

## Verification Results

All voting scenarios now work correctly:

✅ **Upvote increments by 1**: 0 → 1  
✅ **Toggle upvote returns to former value**: 1 → 0  
✅ **Downvote decrements by 1**: 0 → -1  
✅ **Toggle downvote returns to former value**: -1 → 0  
✅ **Vote changes work**: 1 (up) → -1 (down) (delta of -2)  
✅ **Negative values allowed**: Vote count can be negative  
✅ **Immediate UI updates**: Changes visible instantly  
✅ **Persistent after refresh**: Vote states stored in database  

## Files Modified

### Backend
- `backend/app/routers/questions.py` - Added `undo` parameter to vote endpoint
- `backend/app/routers/answers.py` - Added `undo` parameter to vote endpoint  
- `backend/app/data_service.py` - Added `remove_question_vote()` and `remove_answer_vote()` methods

### Frontend
- `frontend/src/services/api.ts` - Fixed `voteQuestion()` and `voteAnswer()` methods to use proper `undo` parameter

## Test Results

```bash
# Comprehensive voting test results:
Initial: 0
After upvote: 1
After removing upvote: 0  
After downvote: -1
After removing downvote: 0
```

The fix ensures Stack Overflow-style voting behavior where each user can have at most one vote (up or down) per question/answer, and can toggle their vote on/off by clicking the same button twice.
