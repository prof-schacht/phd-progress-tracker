# Docker Setup Guide

## Quick Start

The PhD Progress Tracker is fully containerized and can be started with a single command:

```bash
docker-compose up
```

This will start:
- PostgreSQL database (port 5433)
- Redis cache (port 6380)
- FastAPI backend (port 8001)
- React frontend (port 8080)

Access the application at: http://localhost:8080

## Development Setup

For development with hot-reloading:

```bash
docker-compose -f docker-compose.dev.yml up
```

This provides:
- Backend with auto-reload on code changes
- Frontend dev server with hot module replacement (port 5174)
- Volume mounts for live code updates

## Available Commands

We provide a Makefile for common operations:

```bash
make up          # Start production services
make up-dev      # Start development services
make down        # Stop all services
make build       # Rebuild Docker images
make logs        # View service logs
make ps          # Show running containers
make clean       # Remove containers and volumes
make test        # Run all tests
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:
- Database credentials
- JWT secret key
- Email settings (optional)
- CORS origins

## Service URLs

- Frontend: http://localhost:8080 (production) or http://localhost:5174 (dev)
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs
- PostgreSQL: localhost:5433
- Redis: localhost:6380

## Troubleshooting

### Port Conflicts
If you get port binding errors, ensure no other services are using:
- 8080 (nginx frontend)
- 5174 (vite dev server)
- 8001 (FastAPI backend)
- 5433 (PostgreSQL)
- 6380 (Redis)

Note: We use non-standard ports to avoid conflicts with common services.

### Database Connection Issues
The backend waits for PostgreSQL to be healthy before starting. If you see connection errors, check:
- PostgreSQL container logs: `docker-compose logs postgres`
- Database credentials in `.env` file

### Building Issues
If builds fail, try:
1. Clean Docker cache: `docker system prune -a`
2. Rebuild without cache: `docker-compose build --no-cache`

## Production Deployment

For production deployment:
1. Update `.env` with production values
2. Use proper secrets for `SECRET_KEY`
3. Configure SSL/TLS termination
4. Set up proper backup strategies for PostgreSQL
5. Consider using managed services for database and Redis