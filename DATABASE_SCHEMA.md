# Database Schema Documentation

## Overview
This document describes the complete database schema for the Q&A platform. The application uses SQLAlchemy ORM with SQLite/PostgreSQL database, featuring a comprehensive design that supports users, questions, answers, comments, voting, tagging, badges, and analytics.

## Database Tables

### 1. Users Table

**Table Name:** `users`

**Purpose:** Store user account information, profiles, and metadata.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique user identifier |
| `name` | String(50) | UNIQUE, Index, NOT NULL | Username (display name) |
| `email` | String(255) | UNIQUE, Index, NOT NULL | User email address |
| `hashed_password` | String(255) | NOT NULL | Bcrypt hashed password |
| `created_at` | DateTime(timezone=True) | NOT NULL, Default: now() | Account creation timestamp |
| `updated_at` | DateTime(timezone=True) | NOT NULL, Default: now(), OnUpdate: now() | Last update timestamp |
| `reputation` | Integer | NOT NULL, Default: 0 | User reputation score |
| `location` | String(100) | NULLABLE | User location |
| `website` | String(255) | NULLABLE | User website URL |
| `about` | Text | NULLABLE | User bio/description |
| `last_seen` | DateTime(timezone=True) | NOT NULL, Default: now() | Last activity timestamp |
| `is_active` | Boolean | NOT NULL, Default: True | Account active status |
| `is_deleted` | Boolean | NOT NULL, Default: False | Soft delete flag |
| `profile` | JSON | NULLABLE | Structured profile data |

#### Profile JSON Structure
```json
{
  "basic": {
    "displayName": "string",
    "location": "string", 
    "title": "string",
    "pronouns": "string"
  },
  "about": {
    "bio": "string",
    "interests": "string"
  },
  "developer": {
    "primaryLanguage": "string",
    "technologies": "string",
    "yearsOfExperience": "string",
    "githubProfile": "string"
  },
  "links": {
    "website": "string",
    "twitter": "string",
    "github": "string"
  }
}
```

#### Relationships
- **One-to-Many:** `questions` (User can have many questions)
- **One-to-Many:** `answers` (User can have many answers)
- **One-to-Many:** `votes` (User can cast many votes)
- **One-to-Many:** `badges` (User can earn many badges via UserBadge)
- **One-to-Many:** `comments` (User can write many comments)
- **One-to-Many:** `comment_votes` (User can vote on many comments)

---

### 2. Questions Table

**Table Name:** `questions`

**Purpose:** Store questions posted by users.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique question identifier |
| `title` | String | Index | Question title |
| `body` | Text | | Question content/description |
| `author_id` | Integer | FOREIGN KEY → users.id | Question author |
| `created_at` | DateTime | Default: utcnow() | Question creation timestamp |
| `updated_at` | DateTime | Default: utcnow(), OnUpdate: utcnow() | Last update timestamp |
| `votes` | Integer | Default: 0 | Net vote score (upvotes - downvotes) |
| `views` | Integer | Default: 0 | Number of times question was viewed |
| `is_answered` | Boolean | Default: False | Whether question has accepted answer |

#### Relationships
- **Many-to-One:** `author` (Question belongs to one User)
- **One-to-Many:** `answers` (Question can have many answers)
- **Many-to-Many:** `tags` (Question can have many tags via question_tags)
- **One-to-Many:** `question_votes` (Question can receive many votes)
- **One-to-Many:** `comments` (Question can have many comments)

---

### 3. Answers Table

**Table Name:** `answers`

**Purpose:** Store answers to questions.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique answer identifier |
| `body` | Text | | Answer content |
| `author_id` | Integer | FOREIGN KEY → users.id | Answer author |
| `question_id` | Integer | FOREIGN KEY → questions.id | Related question |
| `created_at` | DateTime | Default: utcnow() | Answer creation timestamp |
| `updated_at` | DateTime | Default: utcnow(), OnUpdate: utcnow() | Last update timestamp |
| `votes` | Integer | Default: 0 | Net vote score |
| `is_accepted` | Boolean | Default: False | Whether this is the accepted answer |

#### Relationships
- **Many-to-One:** `author` (Answer belongs to one User)
- **Many-to-One:** `question` (Answer belongs to one Question)
- **One-to-Many:** `answer_votes` (Answer can receive many votes)
- **One-to-Many:** `comments` (Answer can have many comments)

---

### 4. Tags Table

**Table Name:** `tags`

**Purpose:** Store tag definitions for categorizing questions.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique tag identifier |
| `name` | String | UNIQUE, Index | Tag name (e.g., "python", "javascript") |
| `description` | Text | NULLABLE | Tag description |
| `created_at` | DateTime | Default: utcnow() | Tag creation timestamp |
| `count` | Integer | Default: 0 | Number of questions using this tag |

#### Relationships
- **Many-to-Many:** `questions` (Tag can be used by many questions via question_tags)

---

### 5. Question Tags Table (Association Table)

**Table Name:** `question_tags`

**Purpose:** Many-to-many relationship between questions and tags.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `question_id` | Integer | PRIMARY KEY, FOREIGN KEY → questions.id | Question identifier |
| `tag_id` | Integer | PRIMARY KEY, FOREIGN KEY → tags.id | Tag identifier |

#### Composite Primary Key
- (`question_id`, `tag_id`)

---

### 6. Votes Table

**Table Name:** `votes`

**Purpose:** Store voting records for questions and answers.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique vote identifier |
| `user_id` | Integer | FOREIGN KEY → users.id | User who cast the vote |
| `question_id` | Integer | FOREIGN KEY → questions.id, NULLABLE | Voted question (if vote is on question) |
| `answer_id` | Integer | FOREIGN KEY → answers.id, NULLABLE | Voted answer (if vote is on answer) |
| `vote_type` | String | | Vote type: "up" or "down" |
| `created_at` | DateTime | Default: utcnow() | Vote timestamp |

#### Business Logic Constraints
- Either `question_id` OR `answer_id` must be set, not both
- One user can only vote once per question/answer
- Vote type must be "up" or "down"

#### Relationships
- **Many-to-One:** `user` (Vote belongs to one User)
- **Many-to-One:** `question` (Vote can belong to one Question)
- **Many-to-One:** `answer` (Vote can belong to one Answer)

---

### 7. Badges Table

**Table Name:** `badges`

**Purpose:** Define available badges/achievements.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique badge identifier |
| `name` | String | UNIQUE | Badge name |
| `description` | Text | | Badge description |
| `type` | String | | Badge tier: "gold", "silver", "bronze" |
| `created_at` | DateTime | Default: utcnow() | Badge creation timestamp |

#### Relationships
- **One-to-Many:** `users` (Badge can be awarded to many users via UserBadge)

---

### 8. User Badges Table

**Table Name:** `user_badges`

**Purpose:** Many-to-many relationship between users and badges with award timestamp.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique record identifier |
| `user_id` | Integer | FOREIGN KEY → users.id | User who earned the badge |
| `badge_id` | Integer | FOREIGN KEY → badges.id | Badge that was earned |
| `awarded_at` | DateTime | Default: utcnow() | When badge was awarded |

#### Relationships
- **Many-to-One:** `user` (UserBadge belongs to one User)
- **Many-to-One:** `badge` (UserBadge belongs to one Badge)

---

### 9. Comments Table

**Table Name:** `comments`

**Purpose:** Store comments on questions and answers.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique comment identifier |
| `body` | Text | NOT NULL | Comment content |
| `author_id` | Integer | FOREIGN KEY → users.id, NOT NULL | Comment author |
| `question_id` | Integer | FOREIGN KEY → questions.id, NULLABLE | Related question (if comment on question) |
| `answer_id` | Integer | FOREIGN KEY → answers.id, NULLABLE | Related answer (if comment on answer) |
| `created_at` | DateTime | Default: utcnow() | Comment creation timestamp |
| `updated_at` | DateTime | Default: utcnow(), OnUpdate: utcnow() | Last update timestamp |
| `votes` | Integer | Default: 0 | Number of upvotes |

#### Table Constraints
```sql
CHECK CONSTRAINT: (question_id IS NOT NULL AND answer_id IS NULL) OR (question_id IS NULL AND answer_id IS NOT NULL)
```
This ensures a comment is associated with either a question OR an answer, but not both.

#### Relationships
- **Many-to-One:** `author` (Comment belongs to one User)
- **Many-to-One:** `question` (Comment can belong to one Question)
- **Many-to-One:** `answer` (Comment can belong to one Answer)
- **One-to-Many:** `comment_votes` (Comment can receive many votes)

---

### 10. Comment Votes Table

**Table Name:** `comment_votes`

**Purpose:** Store upvotes for comments (comments only support upvotes, not downvotes).

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique vote identifier |
| `user_id` | Integer | FOREIGN KEY → users.id | User who voted |
| `comment_id` | Integer | FOREIGN KEY → comments.id | Voted comment |
| `created_at` | DateTime | Default: utcnow() | Vote timestamp |

#### Business Logic Constraints
- One user can only vote once per comment
- Comments only support upvotes (toggle on/off)

#### Relationships
- **Many-to-One:** `user` (CommentVote belongs to one User)
- **Many-to-One:** `comment` (CommentVote belongs to one Comment)

---

### 11. Analytics Logs Table

**Table Name:** `analytics_logs`

**Purpose:** Store user interaction analytics and events.

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, Index | Unique log identifier |
| `session_id` | String | Index | User session identifier |
| `event_type` | String | | Type of event (e.g., "page_view", "button_click") |
| `event_data` | JSON | | Structured event data |
| `timestamp` | DateTime(timezone=True) | Default: now() | Event timestamp |
| `user_id` | Integer | FOREIGN KEY → users.id, NULLABLE | Associated user (if logged in) |

#### Relationships
- **Many-to-One:** `user` (AnalyticsLog can belong to one User)

---

## Entity Relationship Overview

### Core Content Flow
```
User → Question → Answer → Comment
     ↓         ↓        ↓        ↓
   Vote     Vote    Vote    Vote
```

### Tagging System
```
Question ←→ question_tags ←→ Tag
```

### Reputation System
```
User ←→ user_badges ←→ Badge
```

### Analytics System
```
User → AnalyticsLog
```

## Database Indexes

### Primary Indexes
- All `id` columns (Primary Keys)
- `users.name` (Username lookups)
- `users.email` (Email lookups)
- `questions.title` (Question searches)
- `tags.name` (Tag lookups)
- `analytics_logs.session_id` (Session tracking)

### Foreign Key Indexes
All foreign key columns are automatically indexed for join performance.

## Constraints Summary

### Unique Constraints
- `users.name` - Usernames must be unique
- `users.email` - Email addresses must be unique
- `tags.name` - Tag names must be unique
- `badges.name` - Badge names must be unique

### Check Constraints
- `comments.comment_target_constraint` - Comment must be on question OR answer, not both

### Default Values
- Timestamps default to current time
- Boolean flags default to appropriate values (active=True, deleted=False)
- Counters default to 0 (votes, views, reputation)

## Data Relationships Summary

### One-to-Many Relationships
- User → Questions (1 user can ask many questions)
- User → Answers (1 user can write many answers)
- User → Comments (1 user can write many comments)
- User → Votes (1 user can cast many votes)
- User → CommentVotes (1 user can vote on many comments)
- Question → Answers (1 question can have many answers)
- Question → Comments (1 question can have many comments)
- Question → Votes (1 question can receive many votes)
- Answer → Comments (1 answer can have many comments)
- Answer → Votes (1 answer can receive many votes)
- Comment → CommentVotes (1 comment can receive many votes)

### Many-to-Many Relationships
- Question ↔ Tag (via question_tags table)
- User ↔ Badge (via user_badges table)

### Cascade Delete Behavior
- Deleting a User cascades to delete all their questions, answers, votes, comments
- Deleting a Question cascades to delete all its answers and comments
- Deleting an Answer cascades to delete all its comments

## Database Design Principles

### 1. Normalization
- The schema is normalized to 3NF to reduce redundancy
- Junction tables properly handle many-to-many relationships

### 2. Soft Deletes
- Users have `is_deleted` flag for soft deletion
- Preserves data integrity and historical records

### 3. Audit Trail
- All major entities have `created_at` and `updated_at` timestamps
- Analytics table provides comprehensive event tracking

### 4. Performance Optimization
- Strategic indexing on frequently queried columns
- JSON columns for flexible profile and analytics data

### 5. Data Integrity
- Foreign key constraints maintain referential integrity
- Check constraints enforce business rules
- Appropriate use of nullable vs non-nullable columns

## Sample Queries

### Get User's Questions with Tags
```sql
SELECT q.*, t.name as tag_name 
FROM questions q
JOIN question_tags qt ON q.id = qt.question_id
JOIN tags t ON qt.tag_id = t.id
WHERE q.author_id = ?
```

### Get Question with Answers and Comments
```sql
SELECT q.*, a.*, c.*
FROM questions q
LEFT JOIN answers a ON q.id = a.question_id
LEFT JOIN comments c ON (c.question_id = q.id OR c.answer_id = a.id)
WHERE q.id = ?
```

### Get User's Reputation Summary
```sql
SELECT 
  u.reputation,
  COUNT(DISTINCT q.id) as question_count,
  COUNT(DISTINCT a.id) as answer_count,
  COUNT(DISTINCT v.id) as vote_count
FROM users u
LEFT JOIN questions q ON u.id = q.author_id
LEFT JOIN answers a ON u.id = a.author_id  
LEFT JOIN votes v ON u.id = v.user_id
WHERE u.id = ?
GROUP BY u.id
``` 