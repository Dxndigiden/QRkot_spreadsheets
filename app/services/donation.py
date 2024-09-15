from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import ProjectManagementCRUD, DonationRepository
from .base import BaseProjectService


class DonationManagementService(BaseProjectService):

    def __init__(self, session: AsyncSession):
        super().__init__(
            DonationRepository(),
            ProjectManagementCRUD(),
            session
        )

    async def fetch_donations_by_user(
        self,
        user: models.User,
    ) -> list[models.Donation]:
        donations = await self.main_crud.get_donations_by_user(
            self.session,
            user
        )
        return donations
