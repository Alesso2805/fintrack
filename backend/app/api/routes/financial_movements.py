from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.deps import get_financial_movement_service, require_roles
from app.models.financial import MovementStatus, MovementType
from app.models.user import User, UserRole
from app.schemas.financial import (
    FinancialMovementCreate,
    FinancialMovementRead,
    FinancialMovementUpdate,
)
from app.services.financial_service import FinancialMovementService

router = APIRouter(prefix="/financial-movements", tags=["financial movements"])

read_roles = (UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER)
write_roles = (UserRole.ADMIN, UserRole.ANALYST)


@router.get("", response_model=list[FinancialMovementRead])
async def list_financial_movements(
    investor_id: str | None = None,
    category_id: str | None = None,
    movement_type: MovementType | None = Query(default=None, alias="type"),
    movement_status: MovementStatus | None = Query(default=None, alias="status"),
    date_from: date | None = None,
    date_to: date | None = None,
    _: User = Depends(require_roles(*read_roles)),
    service: FinancialMovementService = Depends(get_financial_movement_service),
) -> list[FinancialMovementRead]:
    return await service.list(
        investor_id=investor_id,
        category_id=category_id,
        movement_type=movement_type,
        movement_status=movement_status,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("", response_model=FinancialMovementRead, status_code=status.HTTP_201_CREATED)
async def create_financial_movement(
    payload: FinancialMovementCreate,
    current_user: User = Depends(require_roles(*write_roles)),
    service: FinancialMovementService = Depends(get_financial_movement_service),
) -> FinancialMovementRead:
    return await service.create(payload, created_by=current_user.id)


@router.get("/{movement_id}", response_model=FinancialMovementRead)
async def get_financial_movement(
    movement_id: str,
    _: User = Depends(require_roles(*read_roles)),
    service: FinancialMovementService = Depends(get_financial_movement_service),
) -> FinancialMovementRead:
    return await service.get_or_404(movement_id)


@router.patch("/{movement_id}", response_model=FinancialMovementRead)
async def update_financial_movement(
    movement_id: str,
    payload: FinancialMovementUpdate,
    _: User = Depends(require_roles(*write_roles)),
    service: FinancialMovementService = Depends(get_financial_movement_service),
) -> FinancialMovementRead:
    return await service.update(movement_id, payload)


@router.delete("/{movement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_financial_movement(
    movement_id: str,
    _: User = Depends(require_roles(*write_roles)),
    service: FinancialMovementService = Depends(get_financial_movement_service),
) -> Response:
    await service.delete(movement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
