from typing import Optional

from pydantic import BaseModel, Extra, validator

from app.models.charity_project import NAME_MAX_LENGTH
from . import BaseTransactionScheme


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: int


class CharityProjectCreate(CharityProjectBase):
    class Config:
        extra = Extra.forbid

    @validator('name')
    def check_name_correct_size(cls, value):
        if not len(value):
            raise ValueError('Название не может быть пустым.')
        if len(value) > NAME_MAX_LENGTH:
            raise ValueError('Название не может быть длиннее '
                             f'{NAME_MAX_LENGTH} символов.')
        return value

    @validator('description')
    def check_description_not_empty(cls, value):
        if not len(value):
            raise ValueError('Описание не может быть пустым.')
        return value

    @validator('full_amount')
    def check_positive_amount(cls, value):
        if not (value > 0):
            raise ValueError('Нельзя внести отрицательное пожертвование!')
        return value


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class CharityProjectDB(BaseTransactionScheme, CharityProjectBase):
    class Config:
        orm_mode = True
