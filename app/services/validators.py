from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.constants import (
    DUBBED_NAME_MSG,
    NOT_REMOVE_MSG,
    NOT_EDIT_MSG,
    NOT_SET_AMOUNT_MSG,
)
from app.crud import ProjectManagementCRUD


async def validate_project_name_unique(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await ProjectManagementCRUD().get_project_by_name(
        project_name,
        session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DUBBED_NAME_MSG,
        )


def validate_project_deletable(
    project: models.CharityProject
) -> None:
    if project.fully_invested or project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_REMOVE_MSG,
        )


def validate_project_updatable(
    project: models.CharityProject,
    update_data: schemas.CharityProjectEdit,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_EDIT_MSG,
        )

    if (update_data.full_amount is not None and
            project.invested_amount > update_data.full_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_SET_AMOUNT_MSG,
        )
