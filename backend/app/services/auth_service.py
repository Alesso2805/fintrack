import jwt
from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import TokenPair
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_service.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        return user

    def issue_token_pair(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            ) from exc

        if payload.get("type") != "refresh" or not payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = await self.user_service.get_by_id(str(payload["sub"]))
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        return self.issue_token_pair(user)
