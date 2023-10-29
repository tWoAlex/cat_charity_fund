# from abc import ABC
from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer

# from app.core.db import Base


def close_date_update(context):
    if context.get_current_parameters().get('fully_invested', False):
        return dt.utcnow()


class BaseTransaction():
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=dt.utcnow)
    close_date = Column(DateTime, default=None, onupdate=close_date_update)
