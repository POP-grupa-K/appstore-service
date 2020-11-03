from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class AppStoreSchema(BaseModel):

    name_app: str
    ranking: Optional[int] = None
    date_update: Optional[datetime] = None
    description_app: Optional[str] = None

    class Config:
        orm_mode = True
