from sqlalchemy import Column, String, Text

from app.core.db import Base

from . import BaseTransaction


NAME_MAX_LENGTH = 100


class CharityProject(Base, BaseTransaction):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
