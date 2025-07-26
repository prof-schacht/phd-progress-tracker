# PhD Progress Tracker - Usage Guide

## Version 0.3.0

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

3. Access the application at:
   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

### First Time Setup

1. Default user accounts (all passwords: password123):
   - Students: john.doe@uni.example.com, jane.smith@uni.example.com, etc.
   - Supervisors: sarah.johnson@uni.example.com, michael.brown@uni.example.com, etc.
   - Admin: admin@uni.example.com

2. Log in with appropriate credentials based on role

3. Create your institution and departments

4. Add supervisors and students

## Core Features

### For Students

#### Reports (Bi-Weekly and Quarterly)
- Access Reports section from navigation menu
- View current period alert showing deadline
- Submit bi-weekly progress updates:
  - Document accomplishments 
  - Report blockers/challenges
  - Plan for next period (auto-filled from previous report)
  - Track time allocation across activities (research, writing, teaching, meetings, other)
- Submit quarterly reviews with additional fields:
  - Key achievements for the quarter
  - Major challenges faced
  - Goals for next quarter
  - Training/workshops completed
  - Private wellbeing notes
- View past reports and their status (submitted, reviewed, overdue)
- Add comments to reports with visibility controls (public, private, supervisor-only)
- Download/export reports for records

#### Research Projects
- Manage multiple research projects
- Set milestones and deadlines
- Track progress visually
- Upload relevant documents

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
curl -X POST "http://localhost:8001/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### Common Endpoints
- `GET /api/v1/dashboard/student` - Student dashboard data
- `GET /api/v1/dashboard/supervisor` - Supervisor dashboard data
- `GET /api/v1/reports/current` - Get current reporting period
- `POST /api/v1/reports/submit` - Submit new report
- `GET /api/v1/users` - List all users (admin only)
- `GET /api/v1/notifications/preferences` - Get notification preferences
- `PUT /api/v1/notifications/preferences` - Update notification preferences
- `GET /api/v1/notifications` - Get in-app notifications
- `PUT /api/v1/notifications/{id}/read` - Mark notification as read
- `POST /api/v1/notifications/test` - Send test notification

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

## Version History

### v0.6.0 (Current)
- Added complete notification UI in frontend
- Created notification dropdown with unread badge
- Implemented notification settings page
- Added test email functionality
- Integrated notification API with React Query
- Added quiet hours and timezone settings

### v0.5.0
- Implemented notification system foundation (Issue #6)
- Added notification preferences API
- Created email notification service with templates
- Added notification models (preferences, logs, reminders)
- Integrated Jinja2 for email templating
- Created in-app notification support

### v0.4.0
- Connected dashboards to real API endpoints
- Fixed supervisor dashboard to use full DashboardService
- Added proper loading states and error handling
- Improved dashboard data display with real-time updates
- Fixed StudentProfile field references (program_name)
- Added year-in-program calculation

### v0.3.0
- Dashboard API endpoints for students and supervisors
- Basic bi-weekly reporting functionality
- User authentication with JWT tokens
- Role-based access control
- Enable caching in production