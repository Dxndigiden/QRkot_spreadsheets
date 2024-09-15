from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from .base import CRUDBase


class DonationRepository(CRUDBase):

    def __init__(self):
        super().__init__(models.Donation)

    async def get_donations_by_user(
        self,
        session: AsyncSession,
        user: models.User,
    ) -> list[models.Donation]:
        query = select(self.model).where(self.model.user_id == user.id)
        result = await session.execute(query)
        return result.scalars().all()
