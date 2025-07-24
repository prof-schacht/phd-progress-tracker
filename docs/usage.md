# PhD Progress Tracker - Usage Guide

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phd-progress-tracker
```

2. Start the application:
```bash
docker-compose up
```

3. Access the application at http://localhost:8080

### First Time Setup

1. The system creates a default admin account:
   - Email: admin@example.com
   - Password: changethis

2. Log in and immediately change the admin password

3. Create your institution and departments

4. Add supervisors and students

## Core Features

### For Students

#### Bi-Weekly Updates
- Submit progress updates every two weeks
- Auto-populated with previous data
- Takes less than 3 minutes to complete
- Track meetings, progress, and blockers

#### Research Projects
- Manage multiple research projects
- Set milestones and deadlines
- Track progress visually
- Upload relevant documents

#### Quarterly Reviews
- Comprehensive progress reviews
- Digital signatures from supervisors
- Export for official records

### For Supervisors

#### Dashboard Overview
- View all supervised students
- Color-coded status indicators
- Overdue update alerts
- Quick access to student profiles

#### Progress Monitoring
- Review bi-weekly updates
- Add comments and feedback
- Track meeting attendance
- Identify at-risk students early

#### Report Generation
- Generate progress reports
- Export student dossiers
- Quarterly review summaries

### For Administrators

#### User Management
- Add/remove users
- Assign roles and permissions
- Manage departments
- Bulk import capabilities

#### Analytics
- Department-wide statistics
- Completion rates
- Trend analysis
- Custom report generation

## API Access

The API is available at http://localhost:8001/api/v1

Interactive documentation: http://localhost:8001/docs

### Authentication
```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### Common Endpoints
- `GET /api/v1/students` - List all students
- `GET /api/v1/reports/bi-weekly` - Get bi-weekly reports
- `POST /api/v1/reports/bi-weekly` - Submit new report
- `GET /api/v1/dashboard/supervisor` - Supervisor dashboard data

## Development

### Running Tests
```bash
make test
```

### Adding New Features
1. Create a feature branch
2. Implement changes
3. Add tests
4. Submit pull request

### Database Migrations
```bash
docker-compose exec backend alembic upgrade head
```

## Troubleshooting

### Cannot Login
- Check credentials are correct
- Ensure cookies are enabled
- Clear browser cache

### Missing Data
- Check user permissions
- Verify data was saved
- Check browser console for errors

### Performance Issues
- Check Docker resource allocation
- Monitor database queries
- Enable caching in production