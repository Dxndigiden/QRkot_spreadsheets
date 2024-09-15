from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.core.constants import MAX_NAME_LENGTH
from .base import DefaultFields


class CharityProject(Base, DefaultFields):

    name = Column(String(MAX_NAME_LENGTH), nullable=False)
    description = Column(Text, nullable=False)
