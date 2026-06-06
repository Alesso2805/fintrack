from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_investor_service, require_roles
from app.models.user import User, UserRole
from app.schemas.financial import InvestorCreate, InvestorRead, InvestorUpdate
from app.services.financial_service import InvestorService

router = APIRouter(prefix="/investors", tags=["investors"])

read_roles = (UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER)
write_roles = (UserRole.ADMIN, UserRole.ANALYST)


@router.get("", response_model=list[InvestorRead])
async def list_investors(
    search: str | None = None,
    _: User = Depends(require_roles(*read_roles)),
    service: InvestorService = Depends(get_investor_service),
) -> list[InvestorRead]:
    return await service.list(search)


@router.post("", response_model=InvestorRead, status_code=status.HTTP_201_CREATED)
async def create_investor(
    payload: InvestorCreate,
    _: User = Depends(require_roles(*write_roles)),
    service: InvestorService = Depends(get_investor_service),
) -> InvestorRead:
    return await service.create(payload)


@router.get("/{investor_id}", response_model=InvestorRead)
async def get_investor(
    investor_id: str,
    _: User = Depends(require_roles(*read_roles)),
    service: InvestorService = Depends(get_investor_service),
) -> InvestorRead:
    return await service.get_or_404(investor_id)


@router.patch("/{investor_id}", response_model=InvestorRead)
async def update_investor(
    investor_id: str,
    payload: InvestorUpdate,
    _: User = Depends(require_roles(*write_roles)),
    service: InvestorService = Depends(get_investor_service),
) -> InvestorRead:
    return await service.update(investor_id, payload)


@router.delete("/{investor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investor(
    investor_id: str,
    _: User = Depends(require_roles(*write_roles)),
    service: InvestorService = Depends(get_investor_service),
) -> Response:
    await service.delete(investor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
