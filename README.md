# PhD Progress Tracker

A lightweight, efficient web application designed to streamline PhD student supervision and progress tracking through regular updates, milestone management, and research pipeline visualization.

## 🎯 Problem Statement

PhD supervisors and students struggle with fragmented progress tracking across emails, spreadsheets, and documents. This leads to:
- Lost context between meetings
- Unclear progress visibility
- Missed deadlines and milestones
- Time-consuming administrative overhead

## 🚀 Solution

PhD Progress Tracker provides a centralized platform that:
- **Reduces reporting overhead** with smart auto-population and quick-update options
- **Improves visibility** through intuitive dashboards and research pipeline tracking
- **Ensures consistency** with automated reminders and structured reporting
- **Supports student success** through milestone tracking and early intervention

## ✨ Key Features

### For PhD Students
- **Bi-weekly micro-updates** in under 3 minutes
- **Research project tracking** with visual pipeline
- **Smart auto-population** from previous updates
- **Personal milestone management** with reminders
- **Mobile-friendly** quick updates
- **Private reflection space** for well-being tracking

### For Supervisors
- **Mission Control Dashboard** - all students at a glance
- **Early warning system** for at-risk students
- **One-click acknowledgments** for routine updates
- **Meeting prep assistant** with auto-generated agendas
- **Batch operations** for managing multiple students
- **Research pipeline overview** across all supervisees

### For Administrators
- **Program-wide analytics** and reporting
- **Configurable workflows** and reminder schedules
- **Compliance tracking** and audit trails
- **Export capabilities** for institutional reporting
- **Cohort management** and bulk operations

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │   API Gateway   │     │   Backend       │
│   (React/Vue)   │────▶│   (FASTAPI)     │────▶│   (Node.js)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │   PostgreSQL    │
                                                 │   Database      │
                                                 └─────────────────┘
```

### Tech Stack
- **Frontend**: React/Vue.js with TypeScript
- **Backend**: Fastapi with Python
- **Database**: PostgreSQL with Redis for caching
- **Authentication**: JWT with optional SSO (SAML/OAuth2)
- **Real-time**: WebSockets for live updates
- **Job Queue**: Bull/BullMQ for reminders and notifications
- **File Storage**: File System object storage

## 📊 Data Model Overview

### Core Entities
- **Users** (students, supervisors, admins(professors))
- **ReportPeriods** (bi-weekly, quarterly)
- **ReportEntries** (actual submissions)
- **ResearchProjects** (papers, experiments, thesis chapters)
- **Milestones** (deadlines, goals, achievements)
- **MeetingNotes** (structured records)
- **Comments** (feedback and discussions)

## 🛠️ Installation

### Prerequisites
- Node.js 18+ 
- PostgreSQL 14+
- Fastapi
- Redis 6+
- npm or yarn

### Quick Start

```bash
# Clone the repository
git clone https://github.com/prof-schacht/phd-progress-tracker.git
cd phd-progress-tracker

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
npm run db:migrate

# Seed sample data (development only)
npm run db:seed

# Start development server
npm run dev
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:3000
```

## 🔧 Configuration

Key configuration options in `.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/phd_tracker
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
REMINDER_CADENCE=biweekly
DEFAULT_TIMEZONE=Europe/Berlin
```

## 🚦 API Overview

### Authentication
```
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

### Reports
```
GET    /api/reports/periods
POST   /api/reports/submit
GET    /api/reports/:id
PUT    /api/reports/:id/comment
```

### Research Projects
```
GET    /api/projects
POST   /api/projects
PUT    /api/projects/:id/status
DELETE /api/projects/:id
```

### Dashboard
```
GET    /api/dashboard/student
GET    /api/dashboard/supervisor
GET    /api/dashboard/analytics
```

## 📱 Screenshots

_Coming soon_

## 🗺️ Roadmap

### Phase 1 (MVP) - 8-10 weeks
- [ ] Core authentication and user management
- [ ] Bi-weekly reporting system
- [ ] Basic dashboards
- [ ] Email reminders
- [ ] Simple exports

### Phase 2 - 6-8 weeks
- [ ] Quarterly review module
- [ ] Research project tracking
- [ ] Advanced analytics
- [ ] Meeting notes integration
- [ ] Slack/Teams notifications

### Phase 3 - Future
- [ ] AI-powered insights
- [ ] Mobile apps
- [ ] Publication integration (ORCID, arXiv)
- [ ] Multi-institution support

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- We use ESLint and Prettier
- Run `npm run lint` before committing
- Follow the existing code patterns

## 📊 Success Metrics

- **Efficiency**: <3 minute bi-weekly updates (from ~15 minutes)
- **Engagement**: >95% consistent reporting rate
- **Satisfaction**: >4.2/5 student satisfaction score
- **Impact**: 50% reduction in status update meetings

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the challenges of PhD supervision in modern academia
- Built with feedback from students and supervisors
- Special thanks to all contributors

## 📞 Support

- **Documentation**: [Wiki](https://github.com/prof-schacht/phd-progress-tracker/wiki)
- **Issues**: [GitHub Issues](https://github.com/prof-schacht/phd-progress-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/prof-schacht/phd-progress-tracker/discussions)

---

**Built with ❤️ for the academic community**
