from sqlalchemy import String, Column, DateTime, Integer, Float

from appstore.schema import appstore_schema
from run import Base


class AppStoreModel(Base):
    __tablename__ = 'appstore'

    id_app = Column('idapp', Integer, primary_key=True)
    name_app = Column('name', String)
    ranking = Column('ranking', Float)
    date_update = Column('dateupdate', DateTime)
    description_app = Column('description', String)
    times_used = Column('timesused', Integer)

    def __init__(self, name_app, ranking, date_update, description_app, times_used):
        self.name_app = name_app
        self.ranking = ranking
        self.date_update = date_update
        self.description_app = description_app
        self.times_used = times_used

    @classmethod
    def from_schema(cls, appstore_schema: appstore_schema.AppStoreSchema):
        return cls(appstore_schema.name_app, appstore_schema.ranking, appstore_schema.date_update, appstore_schema.description_app, appstore_schema.times_used)
