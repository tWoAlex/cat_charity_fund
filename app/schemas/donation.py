from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from . import BaseTransactionScheme


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationCreate(DonationBase):
    class Config:
        orm_mode = True


class DonationDBShort(DonationBase):
    id: int
    create_date: datetime


class DonationDBFull(BaseTransactionScheme, DonationBase):
    pass
