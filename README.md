# Stack Overflow Clone

This is a monorepo containing both the frontend and backend services for a Stack Overflow clone.

## Project Structure

```
.
├── stackoverflow-backend/    # FastAPI backend service
├── stackoverflow-clone/      # Next.js frontend service
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Start the services:
```bash
docker-compose up --build
```

This will start both services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

The services are configured with hot-reloading:
- Frontend changes will automatically reload
- Backend changes will automatically reload

## Stopping the Services

To stop the services:
```bash
docker-compose down
```

## Environment Variables

### Backend
- `ENVIRONMENT`: Set to "development" by default

### Frontend
- `NEXT_PUBLIC_API_URL`: Points to the backend API URL (http://localhost:8000 by default) 