from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import Base
from .base import DefaultFields


class Donation(Base, DefaultFields):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
