from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def create_user(self, payload: UserCreate) -> User:
        user = User(
            email=payload.email.lower(),
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=payload.role,
            is_active=payload.is_active,
        )
        return await self.repository.create(user)
