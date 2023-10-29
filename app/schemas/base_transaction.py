from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseTransactionScheme(BaseModel):
    id: int
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
