from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_my_user(current_user: User = Depends(require_roles(*tuple(UserRole)))) -> User:
    return current_user


@router.get("/admin-check")
async def admin_check(current_user: User = Depends(require_roles(UserRole.ADMIN))) -> dict[str, str]:
    return {"status": "ok", "role": current_user.role}
