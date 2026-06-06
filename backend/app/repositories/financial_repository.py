from datetime import date

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.financial import FinancialMovement, Investor, MovementCategory, MovementStatus, MovementType


class InvestorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, search: str | None = None) -> list[Investor]:
        statement = select(Investor).order_by(Investor.name)
        if search:
            statement = statement.where(Investor.name.ilike(f"%{search}%"))
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, investor_id: str) -> Investor | None:
        return await self.session.get(Investor, investor_id)

    async def get_by_name(self, name: str) -> Investor | None:
        result = await self.session.execute(select(Investor).where(Investor.name == name))
        return result.scalar_one_or_none()

    async def get_by_document_id(self, document_id: str) -> Investor | None:
        result = await self.session.execute(select(Investor).where(Investor.document_id == document_id))
        return result.scalar_one_or_none()

    async def save(self, investor: Investor) -> Investor:
        self.session.add(investor)
        await self.session.commit()
        await self.session.refresh(investor)
        return investor

    async def delete(self, investor: Investor) -> None:
        await self.session.delete(investor)
        await self.session.commit()


class MovementCategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, search: str | None = None) -> list[MovementCategory]:
        statement = select(MovementCategory).order_by(MovementCategory.name)
        if search:
            statement = statement.where(MovementCategory.name.ilike(f"%{search}%"))
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, category_id: str) -> MovementCategory | None:
        return await self.session.get(MovementCategory, category_id)

    async def get_by_name(self, name: str) -> MovementCategory | None:
        result = await self.session.execute(select(MovementCategory).where(MovementCategory.name == name))
        return result.scalar_one_or_none()

    async def save(self, category: MovementCategory) -> MovementCategory:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category: MovementCategory) -> None:
        await self.session.delete(category)
        await self.session.commit()


class FinancialMovementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(
        self,
        investor_id: str | None = None,
        category_id: str | None = None,
        movement_type: MovementType | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[FinancialMovement]:
        statement: Select = select(FinancialMovement).order_by(
            FinancialMovement.movement_date.desc(),
            FinancialMovement.created_at.desc(),
        )
        statement = self._apply_filters(
            statement,
            investor_id=investor_id,
            category_id=category_id,
            movement_type=movement_type,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    def _apply_filters(
        self,
        statement: Select,
        investor_id: str | None = None,
        category_id: str | None = None,
        movement_type: MovementType | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> Select:
        if investor_id:
            statement = statement.where(FinancialMovement.investor_id == investor_id)
        if category_id:
            statement = statement.where(FinancialMovement.category_id == category_id)
        if movement_type:
            statement = statement.where(FinancialMovement.type == movement_type)
        if status:
            statement = statement.where(FinancialMovement.status == status)
        if date_from:
            statement = statement.where(FinancialMovement.movement_date >= date_from)
        if date_to:
            statement = statement.where(FinancialMovement.movement_date <= date_to)
        return statement

    async def get_balances_by_currency(
        self,
        investor_id: str | None = None,
        category_id: str | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        from sqlalchemy import func
        statement = select(
            FinancialMovement.currency,
            func.sum(FinancialMovement.amount).filter(FinancialMovement.type == MovementType.DEPOSIT).label('total_deposits'),
            func.sum(FinancialMovement.amount).filter(FinancialMovement.type == MovementType.WITHDRAWAL).label('total_withdrawals')
        )
        statement = self._apply_filters(
            statement,
            investor_id=investor_id,
            category_id=category_id,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        statement = statement.group_by(FinancialMovement.currency)
        result = await self.session.execute(statement)
        return result.all()

    async def get_category_distribution(
        self,
        investor_id: str | None = None,
        movement_type: MovementType | None = None,
        status: MovementStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        from sqlalchemy import func
        statement = select(
            MovementCategory.id.label('category_id'),
            MovementCategory.name.label('category_name'),
            func.sum(FinancialMovement.amount).label('total_amount')
        ).join(MovementCategory, FinancialMovement.category_id == MovementCategory.id)
        
        statement = self._apply_filters(
            statement,
            investor_id=investor_id,
            movement_type=movement_type,
            status=status,
            date_from=date_from,
            date_to=date_to,
        )
        statement = statement.group_by(MovementCategory.id, MovementCategory.name)
        result = await self.session.execute(statement)
        return result.all()

    async def get(self, movement_id: str) -> FinancialMovement | None:
        return await self.session.get(FinancialMovement, movement_id)

    async def save(self, movement: FinancialMovement) -> FinancialMovement:
        self.session.add(movement)
        await self.session.commit()
        await self.session.refresh(movement)
        return movement

    async def delete(self, movement: FinancialMovement) -> None:
        await self.session.delete(movement)
        await self.session.commit()
