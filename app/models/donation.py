from sqlalchemy import Column, ForeignKey, String

from app.core.db import Base

from . import BaseTransaction


class Donation(Base, BaseTransaction):
    user_id = Column(String, ForeignKey('user.id'))
    comment = Column(String(100), nullable=True)
