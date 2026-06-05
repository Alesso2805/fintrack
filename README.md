# FinTrack API & Dashboard

FinTrack is a portfolio-oriented financial operations platform for registering, categorizing, importing, exporting, and visualizing investor financial movements.

The project is organized as a monorepo:

```text
fintrack/
  backend/          FastAPI, SQLAlchemy, Alembic, PostgreSQL
  frontend/         Next.js dashboard layer, implemented from Phase 6
  docker-compose.yml
  README.md
```

## Implementation Roadmap

### Phase 1 - Current

- Monorepo structure.
- Docker Compose with PostgreSQL and FastAPI backend.
- FastAPI project base.
- SQLAlchemy async database connection.
- Alembic migration setup.
- Health check endpoints.
- Backend test scaffold.

### Phase 2

- JWT authentication with access and refresh tokens.
- Password hashing with bcrypt/passlib.
- RBAC roles: `admin`, `analyst`, `viewer`.
- Initial admin seed.
- Protected endpoints.

### Phase 3

- Investors, movement categories, and financial movements.
- CRUD endpoints.
- Filters and validations.

### Phase 4

- CSV import with row-level validation.
- ImportBatch tracking.
- Partial valid-row loading.

### Phase 5

- Dashboard metrics endpoints.
- CSV report export.

### Phase 6

- Next.js App Router frontend.
- Login, dashboard, movement table, forms, reports, and upload flow.

### Phase 7

- Expanded Pytest coverage.
- GitHub Actions.
- Professional README, screenshots, and endpoint documentation.

## Local Development

Copy the backend environment file:

```bash
cp backend/.env.example backend/.env
```

Start the Phase 1 stack:

```bash
docker compose up --build
```

Backend API:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

Health checks:

```text
GET http://localhost:8000/api/v1/health
GET http://localhost:8000/api/v1/health/db
```
## Security Notes

The repository includes only development defaults for Docker and local setup. Do not use the sample PostgreSQL credentials from `docker-compose.yml` or `.env.example` in production.

Real secrets must stay in local `.env` files, deployment secret managers, or CI/CD secret storage. The local `backend/.env` file is intentionally ignored by Git.
