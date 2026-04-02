# TaskHub

## Overview
TaskHub is a multi-tenant project management system for tracking tasks and team collaboration. It organizes work into a hierarchy of Workspaces, Projects, and Tasks, providing data isolation and role-based access control.

## Architecture
The system consists of three main components:
- **Backend**: A FastAPI REST API that handles business logic, authentication, and data persistence.
- **Frontend**: A Next.js application using the App Router for UI and React Query for server state management.
- **Database**: PostgreSQL for relational storage of users, workspaces, and task data.

## Key Engineering Decisions
- **Multi-tenancy via Workspaces**: Data isolation is enforced at the workspace level. All projects and tasks are scoped to a specific workspace to ensure users only see data relevant to their organization.
- **Stateless Authentication**: JWT-based authentication is used to keep the backend stateless, allowing for easier scaling and avoiding server-side session overhead.
- **ORM Optimization**: SQLAlchemy is used for database interactions. To prevent N+1 query problems, the system utilizes `joinedload` and `subqueryload` for efficient retrieval of nested relationships (e.g., projects within a workspace).
- **Rate Limiting**: Integrated SlowAPI on authentication and sensitive endpoints to protect against brute-force attacks and automated abuse.
- **Audit Logging**: A centralized `ActivityLog` records all major state changes (e.g., task status updates, project archiving) to provide a complete history of system actions.

## Features (Backend)
- **Workspace Isolation**: Logical partitioning of data; membership is required to access workspace resources.
- **Role-Based Access Control (RBAC)**: Permission levels (Owner, Admin, Member, Viewer) manage user actions within workspaces and projects.
- **Task Management Engine**: Supports priorities, status workflows, due dates, and multiple assignees per task.
- **Notification System**: Generates system-wide alerts for task assignments and mentions.
- **Secure Registration**: Email-based OTP (One-Time Password) verification for user onboarding and password recovery.
- **Audit Trail**: Persistent tracking of user actions across the platform.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Pydantic, PyJWT, SlowAPI.
- **Database**: PostgreSQL.
- **Frontend**: Next.js, TailwindCSS, Shadcn UI, React Query.
- **Deployment**: Docker, Docker Compose.

## Workflow / API
1. **Authentication**: User registration triggers an OTP email. Verification is required before the first login, which issues a JWT.
2. **Workspace Management**: Users create workspaces (becoming the Owner) and invite others. Invitations are managed via a dedicated invite model and email flow.
3. **Project Execution**: Projects are created within workspaces. Tasks are then added to projects, assigned to members, and tracked through status transitions.
4. **Activity & Notifications**: System actions trigger `ActivityLog` entries and `Notification` records for relevant users.

## Challenges & Solutions
- **Relational Complexity**: Managing the many-to-many relationships between users, workspaces, and projects while maintaining performance. **Solution**: Optimized database queries using Eager Loading and selective column fetching to minimize payload size and database load.
- **Access Control Enforcement**: Ensuring consistent permission checks across multiple resource types. **Solution**: Implemented reusable FastAPI dependencies that verify user roles and resource ownership before executing route logic.
- **Email Reliability**: Managing OTP delivery and verification flows. **Solution**: Built a structured mailer utility with error handling and logging to ensure visibility into delivery status.

## How to Run
### Using Docker (Recommended)
1. Clone the repository.
2. Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@db:5432/taskhub
   JWT_SECRET=your_jwt_secret
   ALGORITHM=HS256
   FRONTEND_URL=http://localhost:3000
   # SMTP configuration for email/OTP
   ```
3. Run `docker-compose up --build`.
4. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

### Manual Setup
- **Backend**:
  ```bash
  cd backend
  pip install -r requirements.txt
  python app.py
  ```
- **Frontend**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
- **Database**: Ensure a PostgreSQL instance is running and matches the configuration in your `.env` file.
