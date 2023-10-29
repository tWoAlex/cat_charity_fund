from sqlalchemy import Column, String, Text

from app.core.db import Base

from . import BaseTransaction


class CharityProject(Base, BaseTransaction):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
