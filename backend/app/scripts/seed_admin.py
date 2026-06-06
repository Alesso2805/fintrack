import asyncio

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


async def seed_admin() -> None:
    async with AsyncSessionLocal() as session:
        user_service = UserService(UserRepository(session))
        existing_admin = await user_service.get_by_email(settings.initial_admin_email)
        if existing_admin is not None:
            print(f"Admin user already exists: {settings.initial_admin_email}")
            return

        await user_service.create_user(
            UserCreate(
                email=settings.initial_admin_email,
                password=settings.initial_admin_password,
                full_name=settings.initial_admin_full_name,
                role=UserRole.ADMIN,
            )
        )
        print(f"Admin user created: {settings.initial_admin_email}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
