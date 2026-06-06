from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    expires_at = datetime.now(UTC) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "type": token_type, "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    return create_token(
        subject=subject,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
    )


def create_refresh_token(subject: str) -> str:
    return create_token(
        subject=subject,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
    )


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
