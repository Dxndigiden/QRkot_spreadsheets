from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import (
    MIN_FULL_AMOUNT, MIN_DESCRIPTION_LENGTH,
    MIN_NAME_LENGTH, MAX_NAME_LENGTH
)
from .base import ExtendedInvestmentSummary


class CharityProjectDetails(ExtendedInvestmentSummary):

    name: str = Field(
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)


class CharityProjectCreation(BaseModel):

    name: str = Field(
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: str = Field(min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: int = Field(ge=MIN_FULL_AMOUNT)


class CharityProjectUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_DESCRIPTION_LENGTH
    )
    full_amount: Optional[int] = Field(
        None,
        ge=MIN_FULL_AMOUNT
    )

    class Config:

        extra = 'forbid'


class CharityProjectCreate(CharityProjectCreation):

    pass


class CharityProjectEdit(CharityProjectUpdate):

    pass
