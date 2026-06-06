from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.imports import ImportBatch


class ImportBatchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, import_batch: ImportBatch) -> ImportBatch:
        self.session.add(import_batch)
        await self.session.flush()
        await self.session.refresh(import_batch)
        return import_batch

    async def get_by_id(self, batch_id: str) -> ImportBatch | None:
        stmt = select(ImportBatch).where(ImportBatch.id == batch_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> Sequence[ImportBatch]:
        stmt = select(ImportBatch).order_by(ImportBatch.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, import_batch: ImportBatch) -> ImportBatch:
        await self.session.flush()
        await self.session.refresh(import_batch)
        return import_batch
