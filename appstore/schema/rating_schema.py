from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class RatingSchema(BaseModel):
    value: float
    id_app: int
    comm: Optional[str] = None
    date_update: Optional[datetime] = None

    class Config:
        orm_mode = True
