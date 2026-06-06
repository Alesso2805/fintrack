import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-minimum-32-bytes-long"
os.environ["INITIAL_ADMIN_PASSWORD"] = "test-admin-password"

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'test.db'}"
    engine = create_async_engine(database_url)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def prepare_database() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async with TestingSessionLocal() as session:
            user_service = UserService(UserRepository(session))
            await user_service.create_user(
                UserCreate(
                    email="admin@example.com",
                    password="admin-password",
                    full_name="Admin User",
                    role=UserRole.ADMIN,
                )
            )
            await user_service.create_user(
                UserCreate(
                    email="viewer@example.com",
                    password="viewer-password",
                    full_name="Viewer User",
                    role=UserRole.VIEWER,
                )
            )

    async def override_get_db_session() -> AsyncGenerator:
        async with TestingSessionLocal() as session:
            yield session

    asyncio.run(prepare_database())
    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())
