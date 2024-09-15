from datetime import datetime
from typing import Union, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import CRUDBase


class BaseProjectService:

    def __init__(
            self,
            main_crud: CRUDBase,
            aux_crud: CRUDBase,
            session: AsyncSession
    ):
        self.main_crud = main_crud
        self.aux_crud = aux_crud
        self.session = session

    async def get_all(
            self
    ) -> List[Union[models.Donation, models.CharityProject]]:
        projects = await self.main_crud.fetch_all(self.session)
        return projects

    async def create(
        self,
        project_data,
        user: Optional[models.User] = None,
    ) -> Union[models.Donation, models.CharityProject]:
        db_object = await self.main_crud.create(
            project_data.dict(),
            self.session
        )
        await self._invest_in_project(db_object, project_data.full_amount)
        self.session.add(db_object)
        await self.session.commit()
        await self.session.refresh(db_object)
        return db_object

    async def _invest_in_project(
        self, project: models.CharityProject, total_amount: int
    ) -> None:
        transferred_amount = 0
        donations = await self.aux_crud.fetch_opened(self.session)
        for donation in donations:
            available_amount = donation.full_amount - donation.invested_amount
            allocated_amount = min(
                total_amount - transferred_amount,
                available_amount
            )
            donation.invested_amount += allocated_amount
            transferred_amount += allocated_amount
            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
            self.session.add(donation)
            if transferred_amount >= total_amount:
                break
        project.invested_amount += transferred_amount
        if transferred_amount >= total_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
