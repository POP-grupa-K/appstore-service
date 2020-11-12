from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel


class AppStoreSchema(CamelModel):
    id_app: Optional[int] = None
    name_app: str
    ranking: Optional[int] = None
    date_update: Optional[datetime] = None
    description_app: Optional[str] = None

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            json_dict[''.join(word.title() for word in k.split('_'))] = v
        return json_dict

