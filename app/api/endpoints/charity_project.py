from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.services import CharityProjectHandler as ProjectSvc
from app.api.utils import get_project_or_404

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.CharityProjectDetails,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project_data: schemas.CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    created_project = await ProjectSvc(session).create_project(project_data)
    return created_project


@router.get(
    '/',
    response_model=list[schemas.CharityProjectDetails],
    response_model_exclude_none=True,
)
async def list_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await ProjectSvc(session).get_all()
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=schemas.CharityProjectDetails,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    project_data: schemas.CharityProjectEdit,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_project_or_404(project_id, session)

    updated_project = await ProjectSvc(session).update_project(
        charity_project, project_data
    )
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=schemas.CharityProjectDetails,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_project_or_404(project_id, session)
    removed_project = await ProjectSvc(session).delete_project(charity_project)
    return removed_project
