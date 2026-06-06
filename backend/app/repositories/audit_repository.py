from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import ActionLog


class ActionLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, action_log: ActionLog) -> ActionLog:
        self.session.add(action_log)
        await self.session.flush()
        await self.session.refresh(action_log)
        return action_log
