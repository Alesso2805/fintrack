# FinTrack Backend

FastAPI backend for the FinTrack portfolio project.

## Stack

- FastAPI
- SQLAlchemy async
- Alembic
- PostgreSQL
- Pydantic Settings
- Pytest

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

The backend expects PostgreSQL to be available using the `DATABASE_URL` value from `.env`.
