from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.constants import DAYS_IN_MONTH, DAYS_IN_YEAR
from .base import CRUDBase


class ProjectManagementCRUD(CRUDBase):

    def __init__(self):
        super().__init__(models.CharityProject)

    async def update_project(
        self,
        current_project: models.CharityProject,
        project_update: schemas.CharityProjectEdit,
        session: AsyncSession,
    ) -> models.CharityProject:
        project_data = jsonable_encoder(current_project)
        update_data = project_update.dict(exclude_unset=True)

        for field in project_data:
            if field in update_data:
                setattr(current_project, field, update_data[field])

        if (current_project.invested_amount >=
                current_project.full_amount):
            current_project.fully_invested = True
            current_project.close_date = datetime.now()

        session.add(current_project)
        await session.commit()
        await session.refresh(current_project)
        return current_project

    async def delete_project(
        self,
        current_project: models.CharityProject,
        session: AsyncSession,
    ) -> models.CharityProject:
        await session.delete(current_project)
        await session.commit()
        return current_project

    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[models.CharityProject]:
        result = await session.execute(
            select(self.model).where(
                self.model.name == project_name
            )
        )
        return result.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> Optional[List[dict[str, str]]]:
        charity_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested
            )
        )
        charity_projects = charity_projects.scalars().all()
        list_charity_project = []
        for project in charity_projects:
            if project.close_date and project.create_date:
                start_date = (
                    extract('year', project.create_date) * DAYS_IN_YEAR +
                    extract('month', project.create_date) * DAYS_IN_MONTH +
                    extract('day', project.create_date)
                )
                end_date = (
                    extract('year', project.close_date) * DAYS_IN_YEAR +
                    extract('month', project.close_date) * DAYS_IN_MONTH +
                    extract('day', project.close_date)
                )
                time_taken = end_date - start_date
            else:
                time_taken = None
            list_charity_project.append({
                'name': project.name,
                'time_project': time_taken,
                'description': project.description,
            })
        return sorted(list_charity_project, key=lambda i: (i['time_project']))


charity_project_crud = ProjectManagementCRUD()
