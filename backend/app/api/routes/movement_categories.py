from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_movement_category_service, require_roles
from app.models.user import User, UserRole
from app.schemas.financial import MovementCategoryCreate, MovementCategoryRead, MovementCategoryUpdate
from app.services.financial_service import MovementCategoryService

router = APIRouter(prefix="/movement-categories", tags=["movement categories"])

read_roles = (UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER)
write_roles = (UserRole.ADMIN, UserRole.ANALYST)


@router.get("", response_model=list[MovementCategoryRead])
async def list_movement_categories(
    search: str | None = None,
    _: User = Depends(require_roles(*read_roles)),
    service: MovementCategoryService = Depends(get_movement_category_service),
) -> list[MovementCategoryRead]:
    return await service.list(search)


@router.post("", response_model=MovementCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_movement_category(
    payload: MovementCategoryCreate,
    _: User = Depends(require_roles(*write_roles)),
    service: MovementCategoryService = Depends(get_movement_category_service),
) -> MovementCategoryRead:
    return await service.create(payload)


@router.get("/{category_id}", response_model=MovementCategoryRead)
async def get_movement_category(
    category_id: str,
    _: User = Depends(require_roles(*read_roles)),
    service: MovementCategoryService = Depends(get_movement_category_service),
) -> MovementCategoryRead:
    return await service.get_or_404(category_id)


@router.patch("/{category_id}", response_model=MovementCategoryRead)
async def update_movement_category(
    category_id: str,
    payload: MovementCategoryUpdate,
    _: User = Depends(require_roles(*write_roles)),
    service: MovementCategoryService = Depends(get_movement_category_service),
) -> MovementCategoryRead:
    return await service.update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movement_category(
    category_id: str,
    _: User = Depends(require_roles(*write_roles)),
    service: MovementCategoryService = Depends(get_movement_category_service),
) -> Response:
    await service.delete(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
