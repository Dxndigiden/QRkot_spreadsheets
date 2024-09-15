from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.constants import NOT_FOUND_MSG
from app.crud import ProjectManagementCRUD


async def get_project_or_404(
    project_id: int,
    session: AsyncSession,
) -> models.CharityProject:
    project = await ProjectManagementCRUD().fetch_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_MSG,
        )
    return project
