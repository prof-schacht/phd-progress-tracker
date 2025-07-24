# PhD Progress Tracker - Usage Guide

## Current Implementation Status (v0.1.0)

### What's Working

#### Infrastructure
- ✅ **Docker Compose Setup**: All services containerized and orchestrated
- ✅ **PostgreSQL Database**: Running on port 5433 with health checks
- ✅ **Redis Cache**: Running on port 6380 for session/cache management
- ✅ **FastAPI Backend**: Running on port 8001 with basic endpoints
- ✅ **React Frontend**: Vite-based setup with TypeScript and TailwindCSS

#### Backend Features
- Basic FastAPI application structure
- Health check endpoint (`/health`)
- Welcome endpoint (`/`)
- CORS configuration for frontend communication
- Environment-based configuration with Pydantic Settings
- PostgreSQL + AsyncPG for database operations
- Redis integration for caching

#### Frontend Features
- React 18 with TypeScript
- Vite for fast development and building
- Basic API service layer for backend communication
- Environment variable configuration
- Version display in UI
- Folder structure: components, pages, services, utils, types

### Getting Started

#### Using Docker (Recommended)

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Check service status:**
   ```bash
   docker ps
   ```

3. **Access the application:**
   - Backend API: http://localhost:8001
   - Frontend: http://localhost:8080 (when Docker build is fixed)

4. **View logs:**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f backend
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

#### Local Development

1. **Backend Development:**
   ```bash
   cd backend
   # Create virtual environment with uv
   uv sync
   
   # Run development server
   uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend Development:**
   ```bash
   cd frontend
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

### API Endpoints

Currently available endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message with version |
| GET | `/health` | Health check endpoint |

### Environment Variables

#### Backend (.env)
- `PROJECT_NAME`: Application name
- `VERSION`: Application version
- `SECRET_KEY`: JWT secret key
- `POSTGRES_*`: Database connection settings
- `REDIS_*`: Redis connection settings
- `BACKEND_CORS_ORIGINS`: Allowed frontend URLs

#### Frontend (.env)
- `VITE_API_URL`: Backend API URL
- `VITE_APP_NAME`: Application display name
- `VITE_APP_VERSION`: Frontend version

### Troubleshooting

#### Backend Issues
1. **Port already in use:**
   ```bash
   # Check what's using port 8001
   lsof -i :8001
   # Kill the process or change the port in docker-compose.yml
   ```

2. **Database connection errors:**
   - Ensure PostgreSQL container is healthy: `docker ps`
   - Check logs: `docker-compose logs postgres`

#### Frontend Issues
1. **Build errors:**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npm run type-check`

2. **API connection errors:**
   - Verify VITE_API_URL in frontend/.env
   - Check CORS settings in backend

### Next Steps

The following features are planned for implementation:

1. **Authentication System**
   - User registration and login
   - JWT token management
   - Role-based access control

2. **Core Features**
   - Student progress reporting
   - Supervisor dashboards
   - Milestone tracking
   - Meeting notes

3. **Database Schema**
   - User models
   - Report models
   - Research project tracking

For detailed implementation plans, see the GitHub issues:
https://github.com/prof-schacht/phd-progress-tracker/issues