# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Claude.md

This file provides guidance to Claude Code when working with code in this repository.

1. ALWAYS write secure best practice Python code.
2. Always try to write as lean as possible code. Don't blow up the repo. 
4 Iterate function based on test results
5. MOVE Test scripts to the tests folder if they are not already there and ensure that they could be reused for later Tests for code coverage or reruns.
6. ALWAYS commit after each new function is added to our codebase
7. Ensure that you are using uv for isolating environments and packagemanagement
8. Use tree command for project structure. If tree comand not exist install it with command: brew install tree
9. For new and open git issues which should be implemented create first a new branch and work in this branch
10. Ensure that always if a issue is completed pull requests are created.
11. Create a tmp folder for development. And create a scratchpad.md file in this folder to chronologically document the development process.
12. Give the user after each finished step a short advise how to test your implementation. 
13. Always update or create the docs/usage.md file with the newly changed functionality to know how to use the actual implementation.
14. Absolut important keep the repo lean and clean, don't add unnecessary files, don't overengineer.
15. USe Playwright for testing the frontend application. 
16. Make Screenshot of the frontend application to anlayze look and feel using Playwright.
17. Try to read the javascript console using Playwright for debugging.
18. If you have implemented an issue ensure that you update the issue in github and close it.
19. Always update the version build number and show it on the front-end with a build number so that it's clear which version is deployed right now. 

## Project Overview

This is the **PhD Progress Tracker** - a comprehensive web application designed to streamline PhD student supervision and progress tracking. It replaces fragmented tracking methods (emails, spreadsheets) with a centralized platform for students, supervisors, and administrators.

**Current Status**: Basic infrastructure setup completed, ready for core feature implementation.

## Technology Stack

- **Frontend**: React 19 + TypeScript + Vite + TailwindCSS
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy + Alembic
- **Database**: PostgreSQL 16 with Redis for caching
- **Infrastructure**: Docker + Docker Compose + Nginx
- **Authentication**: JWT with role-based access control
- **Testing**: Pytest (backend) + Vitest/Playwright (frontend)

## Project Structure

```
phd-progress-tracker/
├── backend/           # FastAPI Python backend
│   ├── app/          # Application code
│   ├── tests/        # Backend tests
│   └── Dockerfile    # Backend container
├── frontend/         # React TypeScript frontend  
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── Dockerfile    # Frontend container
├── docs/             # Documentation
├── scripts/          # Utility scripts
├── tmp/              # Development files
├── docker-compose.yml     # Production setup
└── docker-compose.dev.yml # Development setup
```

## Development Commands

```bash
# Setup and run
make up              # Start production services
make up-dev          # Start development services
make down            # Stop all services
make build           # Build Docker images
make logs            # View service logs
make test            # Run all tests

# Backend specific
docker-compose exec backend pytest                    # Run backend tests
docker-compose exec backend alembic upgrade head      # Run migrations
docker-compose exec backend alembic revision -m "msg" # Create migration

# Frontend specific  
docker-compose exec frontend-dev npm test             # Run frontend tests
docker-compose exec frontend-dev npm run build        # Build for production
```

## Architecture Notes

### Core Features
- **Bi-weekly Progress Updates**: Quick 3-minute updates with smart auto-population
- **Research Project Tracking**: Multiple projects with milestones and deadlines
- **Quarterly Reviews**: Comprehensive reviews with digital signatures
- **Real-time Dashboards**: Supervisor views with early warning indicators
- **File Management**: Document uploads and dossier exports

### API Design
- RESTful API with OpenAPI documentation
- JWT-based authentication with refresh tokens
- Role-based access control (Student, Supervisor, Admin)
- Pagination, filtering, and sorting on all list endpoints
- Comprehensive error handling with proper HTTP status codes

### Database Schema
- **users**: Authentication and user profiles
- **students/supervisors**: Role-specific data
- **bi_weekly_reports**: Regular progress updates
- **research_projects**: Project details and milestones
- **quarterly_reviews**: Formal review records
- **files**: Document storage metadata

## Environment Configuration

Key environment variables (see `.env.example`):
- `SECRET_KEY`: JWT signing key (change in production!)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SMTP_*`: Email configuration (optional)
- `FIRST_SUPERUSER`: Initial admin account

## Development Workflow

### Git Conventions
- Feature branches: `feature/issue-number-description`
- Commit format: `type: description` (feat:, fix:, docs:, etc.)
- Create PR when feature is complete
- All tests must pass before merge

### Testing Strategy
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests with Playwright for critical user flows
- Maintain >80% code coverage

## Key Implementation Guidelines

### Security
- Never store passwords in plain text
- Validate all user inputs
- Use parameterized queries
- Implement rate limiting
- Secure file upload with type validation

### Performance
- Use database indexes on frequently queried fields
- Implement Redis caching for expensive operations
- Paginate all list endpoints
- Optimize N+1 queries with eager loading

### User Experience
- Responsive design for all devices
- Loading states for async operations
- Clear error messages
- Auto-save for long forms
- Offline capability considerations

## Current Implementation Status

✅ Completed:
- Project structure and Docker setup
- Basic FastAPI backend with health check
- React frontend initialization
- Development and production configurations
- Documentation structure

🔄 In Progress:
- Issue #1: Basic infrastructure setup

📋 Upcoming (High Priority):
- Issue #2: User authentication system
- Issue #3: Database models
- Issue #4: Bi-weekly reporting system
- Issue #5: Student and supervisor dashboards

## Testing Your Implementation

After implementing a feature:
1. Run backend tests: `docker-compose exec backend pytest`
2. Run frontend tests: `docker-compose exec frontend-dev npm test`
3. Test manually: Access http://localhost:5174 (dev) or http://localhost:8080 (prod)
4. Check API docs: http://localhost:8001/docs

## Port Configuration

The application uses non-standard ports to avoid conflicts:
- Frontend: 8080 (production) / 5174 (development)
- Backend API: 8001
- PostgreSQL: 5433
- Redis: 6380

These ports are configured to avoid conflicts with other applications running on standard ports.

## Development Notes

- Remember that the actual implementation is using docker-compose all test and updates should be tested against the containers.