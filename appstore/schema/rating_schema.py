from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class RatingSchema(BaseModel):
    value: float = None
    id_rating: int = None
    id_app: Optional[int] = None
    comm: Optional[str] = None
    date_update: Optional[datetime] = None

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            capitalized = ''.join(word.title() for word in k.split('_'))
            json_dict[capitalized[0].lower() + capitalized[1:]] = v
        return json_dict
