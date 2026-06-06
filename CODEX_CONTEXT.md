# Codex Context - FinTrack API & Dashboard

This document gives Codex the project context needed to continue development without losing the thread.

## Project Location

```text
C:\Users\USER\Documents\GitHub\new\fintrack
```

## Project Name

FinTrack API & Dashboard

## Project Goal

Build a portfolio-grade financial operations platform for registering, categorizing, importing, exporting, and visualizing investor/client financial movements.

The project should look professional and credible for a backend/frontend portfolio. It should connect with real financial/reporting experience: investor movements, automated reports, dashboards, APIs, authentication, and structured financial data.

## Monorepo Structure

```text
fintrack/
  backend/
  frontend/
  docker-compose.yml
  README.md
  CODEX_CONTEXT.md
```

## Current Status

Phase 1, Phase 2, and Phase 3 have been implemented and verified.

Implemented:

- Monorepo structure.
- Backend FastAPI base.
- PostgreSQL service through Docker Compose.
- SQLAlchemy async engine and session setup.
- Alembic base setup.
- Pydantic Settings configuration.
- Health check endpoints.
- Backend test scaffold.
- Root README.
- Git initialized locally.
- `.gitignore` configured.
- `backend/.dockerignore` configured.
- `backend/.env` exists locally but is ignored by Git.
- `.env.example` and `backend/.env.example` are safe to commit because they contain placeholders, not real secrets.
- Frontend exists only as a placeholder. No Next.js app has been created yet.
- Authentication and authorization are implemented.
- `User` model exists with roles: `admin`, `analyst`, `viewer`.
- JWT access and refresh tokens are implemented.
- Password hashing uses passlib with bcrypt.
- Auth endpoints exist for login, refresh, and current user.
- RBAC dependencies and protected sample routes exist.
- Initial admin seed script exists.
- Alembic migration for users exists.
- Phase 3 business entities are implemented:
  - `Investor`
  - `MovementCategory`
  - `FinancialMovement`
- CRUD endpoints exist for investors, movement categories, and financial movements.
- Financial movement filters exist for investor, category, type, status, and date range.
- Phase 3 Alembic migration exists and has been applied locally.

Verified:

```text
docker compose exec --workdir /app backend python -m pytest
8 passed
```

Docker stack was also verified successfully:

```text
docker compose up -d --build
```

Health checks responded successfully:

```text
GET http://localhost:8000/api/v1/health
GET http://localhost:8000/api/v1/health/db
POST http://localhost:8000/api/v1/auth/login
```

## Current URLs

```text
Backend: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/api/v1/health
DB Health: http://localhost:8000/api/v1/health/db
Login: http://localhost:8000/api/v1/auth/login
Current User: http://localhost:8000/api/v1/auth/me
Investors: http://localhost:8000/api/v1/investors
Movement Categories: http://localhost:8000/api/v1/movement-categories
Financial Movements: http://localhost:8000/api/v1/financial-movements
```

## Important Docker Commands

Start stack:

```bash
cd C:\Users\USER\Documents\GitHub\new\fintrack
docker compose up -d --build
```

Stop stack:

```bash
cd C:\Users\USER\Documents\GitHub\new\fintrack
docker compose down
```

Check services:

```bash
docker compose ps
```

## GitHub Readiness

The repository is ready for first commit and GitHub upload.

Do not commit:

- `backend/.env`
- `__pycache__/`
- `.pytest_cache/`
- `*.egg-info/`
- `.venv/`
- `node_modules/`
- `.next/`

The `.gitignore` and `backend/.dockerignore` already cover these.

Docker Compose and backend settings require secrets from ignored `.env` files or deployment environment variables. Do not hardcode database passwords, JWT secrets, or initial admin passwords in committed files.

First commit command:

```bash
git add .
git commit -m "Initial FinTrack monorepo setup"
```

Remote setup example:

```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/fintrack.git
git push -u origin main
```

## Closed Technical Decisions

### Database

Use PostgreSQL for the main project because it fits well with FastAPI, SQLAlchemy, Alembic, Docker, and portfolio deployment workflows.

### Authentication

Use JWT authentication with:

- Access token.
- Refresh token.
- Password hashing with bcrypt/passlib.
- Initial users created by seed/admin.
- No public registration in the first version.

### Roles / RBAC

Use three roles:

- `admin`: manages users, investors/clients, movements, categories, imports, and reports.
- `analyst`: manages investors/clients, movements, imports, and reports.
- `viewer`: read-only access to dashboard, movements, and reports.

### Initial Entities

- `User`
- `Investor`
- `FinancialMovement`
- `MovementCategory`
- `ImportBatch`
- `ActionLog`

### FinancialMovement Fields

Minimum fields:

- `id`
- `investor_id`
- `category_id`
- `type`
- `amount`
- `currency`
- `status`
- `movement_date`
- `description`
- `created_by`
- `created_at`
- `updated_at`

### Import MVP

Start with CSV only.

CSV import must:

- Validate required columns.
- Register row-level errors.
- Allow valid rows to load when possible.
- Keep Excel as a future enhancement.

### Export MVP

Start with CSV export.

Future enhancement:

- Basic PDF export using `reportlab`, including summary, applied filters, and table of results.

### Dashboard Metrics

Initial metrics:

- Total movements.
- Total amount by type.
- Amount by status.
- Top investors/clients by volume.
- Recent movements.
- Monthly trend.

### Frontend Stack

Frontend will be implemented later, in Phase 6.

Chosen stack:

- Next.js with App Router.
- React.
- TypeScript.
- Tailwind CSS.
- TanStack Table.
- React Hook Form.
- Zod.
- Recharts.
- Fetch wrapper or Axios for API consumption.

### DevOps

Use:

- Docker for backend, frontend, and PostgreSQL.
- Docker Compose.
- Alembic for migrations.
- GitHub Actions for backend tests.
- `.env.example` files for documented configuration.

Ports:

- Backend: `localhost:8000`
- Frontend: `localhost:3000`
- PostgreSQL external default for local tools: `localhost:5433`

## Implementation Roadmap

### Phase 1 - Done

Create structure of the monorepo, Docker Compose, backend base with FastAPI, PostgreSQL connection, SQLAlchemy, Alembic, and health check.

### Phase 2 - Done

Implement authentication and authorization:

- `User` model.
- Role enum or role model, depending on clean architecture needs.
- Password hashing with passlib/bcrypt.
- JWT access token.
- JWT refresh token.
- Login endpoint.
- Token refresh endpoint.
- Current user endpoint.
- RBAC dependencies.
- Initial admin seed.
- Protected sample endpoint or route protection pattern.
- Alembic migration for users/auth tables.
- Tests for auth happy path and basic failures.

Seed admin:

```text
Configured through INITIAL_ADMIN_EMAIL and INITIAL_ADMIN_PASSWORD.
The password must come from an ignored .env file or a deployment secret manager.
```

Implemented backend structure for Phase 2:

```text
backend/app/
  api/
    deps.py
    routes/
      auth.py
      users.py
  core/
    config.py
    security.py
  db/
    base.py
    session.py
  models/
    user.py
  schemas/
    auth.py
    user.py
  services/
    auth_service.py
    user_service.py
  repositories/
    user_repository.py
  scripts/
    seed_admin.py
```

Keep the architecture clean but pragmatic. Do not over-engineer. Prefer clear service/repository separation only where it helps testability and future CRUD expansion.

### Phase 3 - Done

Implement primary business entities:

- `Investor`
- `MovementCategory`
- `FinancialMovement`

Include:

- CRUD endpoints.
- Filters by date, investor, movement type, and status.
- Validations.
- Alembic migrations.
- Tests.

### Phase 4 - Next

Implement CSV import:

- `ImportBatch` model.
- CSV upload endpoint.
- Required column validation.
- Row-level validation errors.
- Partial success when possible.
- Audit/action logs where appropriate.

### Phase 5

Implement dashboard endpoints and CSV export:

- Metrics summary endpoint.
- Recent movements endpoint or embedded dashboard response.
- Monthly trend endpoint.
- CSV export endpoint with filters.

### Phase 6

Create frontend with Next.js:

- Login page.
- Authenticated dashboard.
- Metric cards.
- Charts using Recharts.
- Movements table using TanStack Table.
- Create/edit movement forms using React Hook Form + Zod.
- Reports view.
- CSV upload view.
- Responsive UI.

Do not build frontend before backend endpoints are ready enough to test real flows.

### Phase 7

Polish for portfolio:

- Expanded Pytest coverage.
- GitHub Actions for backend tests.
- Professional README.
- Endpoint documentation.
- Screenshots.
- Possible deployment notes.

## Development Principles

- Prioritize backend correctness before frontend UI.
- Keep MVP focused and avoid advanced features too early.
- Favor clean, readable architecture over unnecessary abstraction.
- Keep every phase testable.
- Keep `.env` files out of Git.
- Do not add public registration in the first version.
- Do not build the frontend until Phase 6 unless explicitly requested.

## How To Resume With Codex

When returning to this project, tell Codex:

```text
Read CODEX_CONTEXT.md in C:\Users\USER\Documents\GitHub\new\fintrack and continue with Phase 4.
```

Codex should first inspect the current file tree and Git status, then continue with Phase 4 implementation.
