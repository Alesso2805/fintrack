from datetime import date

from fastapi import HTTPException, status

from app.models.financial import FinancialMovement, Investor, MovementCategory, MovementStatus, MovementType
from app.repositories.financial_repository import (
    FinancialMovementRepository,
    InvestorRepository,
    MovementCategoryRepository,
)
from app.schemas.financial import (
    FinancialMovementCreate,
    FinancialMovementUpdate,
    InvestorCreate,
    InvestorUpdate,
    MovementCategoryCreate,
    MovementCategoryUpdate,
)


class InvestorService:
    def __init__(self, repository: InvestorRepository) -> None:
        self.repository = repository

    async def list(self, search: str | None = None) -> list[Investor]:
        return await self.repository.list(search)

    async def get_or_404(self, investor_id: str) -> Investor:
        investor = await self.repository.get(investor_id)
        if investor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investor not found")
        return investor

    async def create(self, payload: InvestorCreate) -> Investor:
        await self._ensure_unique(payload.name, payload.document_id)
        return await self.repository.save(Investor(**payload.model_dump()))

    async def update(self, investor_id: str, payload: InvestorUpdate) -> Investor:
        investor = await self.get_or_404(investor_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data or "document_id" in data:
            await self._ensure_unique(
                data.get("name", investor.name),
                data.get("document_id", investor.document_id),
                current_id=investor.id,
            )
        for field, value in data.items():
            setattr(investor, field, value)
        return await self.repository.save(investor)

    async def delete(self, investor_id: str) -> None:
        await self.repository.delete(await self.get_or_404(investor_id))

    async def _ensure_unique(
        self,
        name: str,
        document_id: str | None,
        current_id: str | None = None,
    ) -> None:
        existing_name = await self.repository.get_by_name(name)
        if existing_name is not None and existing_name.id != current_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Investor name already exists")
        if document_id:
            existing_document = await self.repository.get_by_document_id(document_id)
            if existing_document is not None and existing_document.id != current_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Investor document_id already exists",
                )


class MovementCategoryService:
    def __init__(self, repository: MovementCategoryRepository) -> None:
        self.repository = repository

    async def list(self, search: str | None = None) -> list[MovementCategory]:
        return await self.repository.list(search)

    async def get_or_404(self, category_id: str) -> MovementCategory:
        category = await self.repository.get(category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement category not found")
        return category

    async def create(self, payload: MovementCategoryCreate) -> MovementCategory:
        await self._ensure_unique(payload.name)
        return await self.repository.save(MovementCategory(**payload.model_dump()))

    async def update(self, category_id: str, payload: MovementCategoryUpdate) -> MovementCategory:
        category = await self.get_or_404(category_id)
        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            await self._ensure_unique(data["name"], current_id=category.id)
        for field, value in data.items():
            setattr(category, field, value)
        return await self.repository.save(category)

    async def delete(self, category_id: str) -> None:
        await self.repository.delete(await self.get_or_404(category_id))

    async def _ensure_unique(self, name: str, current_id: str | None = None) -> None:
        existing = await self.repository.get_by_name(name)
        if existing is not None and existing.id != current_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movement category name already exists")


class FinancialMovementService:
    def __init__(
        self,
        movement_repository: FinancialMovementRepository,
        investor_repository: InvestorRepository,
        category_repository: MovementCategoryRepository,
    ) -> None:
        self.movement_repository = movement_repository
        self.investor_repository = investor_repository
        self.category_repository = category_repository

    async def list(
        self,
        investor_id: str | None = None,
        category_id: str | None = None,
        movement_type: MovementType | None = None,
        movement_status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[FinancialMovement]:
        if date_from and date_to and date_from > date_to:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="date_from cannot be after date_to")
        return await self.movement_repository.list(
            investor_id=investor_id,
            category_id=category_id,
            movement_type=movement_type,
            status=movement_status,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_or_404(self, movement_id: str) -> FinancialMovement:
        movement = await self.movement_repository.get(movement_id)
        if movement is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Financial movement not found")
        return movement

    async def create(self, payload: FinancialMovementCreate, created_by: str) -> FinancialMovement:
        await self._ensure_references(payload.investor_id, payload.category_id)
        return await self.movement_repository.save(
            FinancialMovement(**payload.model_dump(), created_by=created_by)
        )

    async def update(self, movement_id: str, payload: FinancialMovementUpdate) -> FinancialMovement:
        movement = await self.get_or_404(movement_id)
        data = payload.model_dump(exclude_unset=True)
        investor_id = data.get("investor_id", movement.investor_id)
        category_id = data.get("category_id", movement.category_id)
        if "investor_id" in data or "category_id" in data:
            await self._ensure_references(investor_id, category_id)
        for field, value in data.items():
            setattr(movement, field, value)
        return await self.movement_repository.save(movement)

    async def delete(self, movement_id: str) -> None:
        await self.movement_repository.delete(await self.get_or_404(movement_id))

    async def _ensure_references(self, investor_id: str, category_id: str) -> None:
        if await self.investor_repository.get(investor_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Investor not found")
        if await self.category_repository.get(category_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement category not found")
