from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from . import BaseTransactionScheme


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: int


class CharityProjectCreate(CharityProjectBase):
    class Config:
        extra = Extra.forbid

    @validator('full_amount')
    def check_positive_amount(cls, value):
        if not (value > 0):
            raise ValueError('Нельзя внести отрицательное пожертвование! 😿')
        return value


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class CharityProjectDB(BaseTransactionScheme, CharityProjectBase):
    class Config:
        orm_mode = True
