from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.services import DonationManagementService as DonationSvc

router = APIRouter()


@router.post(
    '/',
    response_model=schemas.DonationCreationOutput,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_data: schemas.DonationCreationInput,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(current_user),
):
    donation = await DonationSvc(session).create(donation_data, user)
    return donation


@router.get(
    '/',
    response_model=list[schemas.DonationListOutput],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def list_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await DonationSvc(session).get_all()
    return donations


@router.get(
    '/my',
    response_model=list[schemas.DonationListByUserOutput],
    response_model_exclude_none=True,
)
async def list_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(current_user),
):
    donations = await DonationSvc(session).fetch_donations_by_user(user)
    return donations
