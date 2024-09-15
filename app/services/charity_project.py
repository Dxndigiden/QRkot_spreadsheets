from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud import ProjectManagementCRUD, DonationRepository
from .base import BaseProjectService
from .validators import (
    validate_project_name_unique,
    validate_project_deletable,
    validate_project_updatable,
)


class CharityProjectHandler(BaseProjectService):

    def __init__(self, session: AsyncSession):
        super().__init__(
            ProjectManagementCRUD(),
            DonationRepository(),
            session
        )

    async def create_project(
        self,
        project_data: schemas.CharityProjectCreate,
    ) -> models.CharityProject:
        await validate_project_name_unique(project_data.name, self.session)
        charity_project = await super().create(project_data)
        return charity_project

    async def update_project(
        self,
        charity_project: models.CharityProject,
        project_data: schemas.CharityProjectEdit,
    ) -> models.CharityProject:
        validate_project_updatable(charity_project, project_data)
        if (
            project_data.name is not None and
            project_data.name != charity_project.name
        ):
            await validate_project_name_unique(project_data.name, self.session)
        updated_project = await self.main_crud.update_project(
            charity_project, project_data, self.session
        )
        return updated_project

    async def delete_project(
        self,
        charity_project: models.CharityProject,
    ) -> models.CharityProject:
        validate_project_deletable(charity_project)
        deleted_project = await self.main_crud.delete_project(
            charity_project, self.session
        )
        return deleted_project
