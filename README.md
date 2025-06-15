# Stack Overflow Clone

A full-stack Q&A platform built for the "Build, Vibe, Ship!" sprint. It recreates the core experience of Stack Overflow while running entirely locally in Docker. The application ships with realistic mock data, JWT authentication, analytics logging and a complete REST API.

## Key Features

- Landing page pre-populated with seeded questions
- Secure user registration & login (JWT bearer tokens)
- Create new questions with tag support
- Answer questions and comment on both questions and answers
- Up-vote / down-vote questions & answers and toggle up-votes on comments
- Accept an answer and automatically mark the question as solved
- Rich user profiles: editable bio, links, developer stats and reputation
- Profile pages list all questions and answers written by the user
- Badge & reputation system
- Synthetic analytics logging for every significant user action
- Fully documented REST API & database schema

## Tech Stack

**Frontend**
- Next.js 13 (React, TypeScript)
- Tailwind CSS & shadcn/ui
- SWR / React-Query for data fetching

**Backend**
- Python 3.11 + FastAPI
- SQLAlchemy ORM with PostgreSQL (SQLite fallback for dev)
- Alembic migrations & Faker seed script
- JWT (HS256) authentication
- Pydantic models & automatic OpenAPI docs
- Synthetic analytics middleware

**DevOps**
- Docker & Docker-Compose
- Hot-reloading in both services

## Repository Layout

```text
.
├── stackoverflow-backend/    # FastAPI backend service
│   ├── app/                  # API, models, database & seeds
│   └── tests/                # Backend tests
├── stackoverflow-clone/      # Next.js frontend service
│   ├── src/                  # Components, pages, hooks, utils
│   └── tests/                # Front-end & E2E tests
├── docker-compose.yml        # Multi-service orchestration
├── API_DOCUMENTATION.md      # Complete REST API reference 🚀
├── DATABASE_SCHEMA.md        # ER-diagram & table definitions 📚
└── README.md                 # You are here
```

## Getting Started

Prerequisites:
- Docker ≥ 24
- Docker Compose plugin

1. Clone the repo and start the stack

```bash
git clone <repository-url>
cd <repository-name>
docker-compose up --build
```

2. Open your browser:
   - Frontend: http://localhost:3000
   - Backend docs (Swagger): http://localhost:8000/docs

The database is automatically seeded with sample users, tags, questions and answers so you can explore the UI right away.

### Environment Variables

| Service  | Variable              | Default                 | Purpose                |
|----------|-----------------------|-------------------------|------------------------|
| Backend  | `ENVIRONMENT`         | development             | FastAPI environment    |
| Frontend | `NEXT_PUBLIC_API_URL` | http://localhost:8000   | Backend base URL       |

## Feature Walkthrough

1. Landing page shows a list of pre-seeded questions.
2. Sign-up (`Register`) with username, e-mail and password → automatic login.
3. Post an answer or add a comment to any question.
4. Ask a completely new question from the **Ask Question** button.
5. Inside a question page you can:
   - Post answers
   - Comment on the question or any answer
   - Up-vote / down-vote content or retract a vote
6. Click the avatar initials in the nav-bar to open your **Profile** where you can:
   - Edit profile details (bio, links, tech stack, pronouns etc.)
   - Inspect live reputation, badge counts and other stats
   - Browse all your questions & answers

## REST API at a Glance

The backend follows JSON REST conventions and every endpoint is documented in `API_DOCUMENTATION.md` as well as the live Swagger UI.

Most frequently used endpoints:

- `POST /auth/register` / `POST /auth/login` – create account & obtain JWT
- `GET  /questions/` – list questions (`sort`, `tag`, `skip`, `limit` query params)
- `POST /questions/` – create question (bearer token required)
- `GET  /questions/{id}` – get single question (includes answers)
- `POST /answers/` – answer a question
- `POST /questions/{id}/vote` and `/answers/{id}/vote` – voting
- `POST /comments/` – comment on question or answer

For the complete spec including request/response samples and error codes please read [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

## Database Design

The relational data-model is described in [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md).

Highlights:

- 11 core tables (`users`, `questions`, `answers`, `comments`, `votes`, `tags`, …)
- Many-to-many tag system via `question_tags`
- Reputation & badges via `votes` + `user_badges`
- Soft-deletes and timestamp audit fields on all primary entities
- Analytics events stored separately in `analytics_logs`

## Synthetic Control Endpoints (`/_synthetic/*`)

Because this project originates from the **Build, Vibe, Ship!** template it still exposes a small control surface used by automated graders or agents:

| Endpoint                         | Description                                        |
|----------------------------------|----------------------------------------------------|
| `POST /_synthetic/new_session`   | Start isolated session, returns `session_id`       |
| `POST /_synthetic/log_event`     | Ingest custom analytics event                      |
| `GET  /_synthetic/logs`          | Retrieve logs for a session                        |
| `POST /_synthetic/reset`         | Reset environment & reseed database                |

See the backend `routes/synthetic.py` for full payload examples.

## Development

```bash
# Backend
cd stackoverflow-backend
uvicorn app.main:app --reload

# Frontend
cd stackoverflow-clone
npm install
npm run dev
```

Changes are hot-reloaded automatically. Unit tests live under each service's `tests` directory and can be executed via `pytest` (backend) and `npm test` (frontend).

## License

MIT © 2024 Your Name

---

Happy hacking — and may your answers always be accepted! ✨ 