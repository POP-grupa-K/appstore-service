from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel


class AppStoreSchema(CamelModel):
    id_app: Optional[int] = None
    name_app: str
    ranking: Optional[float] = None
    date_update: Optional[datetime] = None
    description_app: Optional[str] = None
    times_used: Optional[int] = 0

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            capitalized = ''.join(word.title() for word in k.split('_'))
            json_dict[capitalized[0].lower() + capitalized[1:]] = v
        return json_dict

