# Ask Question Feature Documentation

## Overview

This document describes the implementation of the "Ask Question" feature for our Stack Overflow clone. The feature allows users to create new questions with a title, body content, and tags.

## Components

The feature consists of the following components:

1. **QuestionForm Component** (`/src/components/QuestionForm.tsx`)
   - A form component that handles user input for creating a new question
   - Validates required fields (title, body, tags)
   - Provides tag suggestions and management
   - Handles form submission

2. **Ask Question Page** (`/src/app/ask/page.tsx`)
   - Simple wrapper page that renders the QuestionForm component
   - Provides the route `/ask` for the form

3. **API Service Integration** (`/src/services/api.ts`)
   - `createQuestion` method that posts the question data to the backend
   - Properly formats the data to match backend expectations

## User Flow

1. User clicks "Ask Question" button on the main page
2. User is redirected to the `/ask` route
3. User fills out the question form:
   - Title (required)
   - Body/details (required)
   - Tags (at least one required, maximum 5)
4. User submits the form
5. If successful, the user is redirected to the newly created question page
6. If there's an error, appropriate feedback is displayed

## Data Model

The question form collects:
- **title**: String (15-150 characters)
- **body**: String (minimum 20 characters)
- **tags**: Array of strings (1-5 tags)

This data is then sent to the backend as:
```json
{
  "title": "Question title",
  "body": "Question content details",
  "author_id": 1,
  "tags": ["tag1", "tag2"]
}
```

## UI Features

The QuestionForm component includes:
- Input validation with error messages
- Character count for title
- Tag suggestions as you type
- Simple markdown toolbar (bold, italic, code, etc.)
- Preview of entered markdown (future enhancement)

## Error Handling

The form handles the following error scenarios:
- Missing required fields
- Backend API errors
- Network errors

Error messages are displayed prominently at the top of the form.

## Future Enhancements

Planned improvements:
- Real-time markdown preview
- Better tag suggestions based on question content
- Question draft saving
- Similar questions suggestions to reduce duplicates
- Rich text editor with more formatting options
