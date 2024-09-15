from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import MIN_FULL_AMOUNT
from .base import InvestmentSummary, ExtendedInvestmentSummary


class DonationCreationInput(BaseModel):

    full_amount: int = Field(ge=MIN_FULL_AMOUNT)
    comment: Optional[str] = None


class FullDonationOutput(ExtendedInvestmentSummary):

    comment: Optional[str] = None
    user_id: int


class ShortenedDonationOutput(InvestmentSummary):

    comment: Optional[str] = None


class DonationListOutput(FullDonationOutput):

    pass


class DonationListByUserOutput(ShortenedDonationOutput):

    pass


class DonationCreationOutput(ShortenedDonationOutput):

    pass
