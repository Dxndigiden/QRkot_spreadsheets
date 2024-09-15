from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def fetch_by_id(self, obj_id: int, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def fetch_all(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def fetch_opened(
        self, session: AsyncSession
    ) -> list[models.Donation]:
        result = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            )
        )
        return result.scalars().all()

    async def create(self, data: dict, session: AsyncSession):
        instance = self.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
