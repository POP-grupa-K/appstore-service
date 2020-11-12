from sqlalchemy import String, Column, DateTime, Integer, Float

from appstore.schema import appstore_schema
from run import Base


class AppStoreModel(Base):
    __tablename__ = 'appstore'

    id_app = Column('idapp', Integer, primary_key=True)
    name_app = Column(String)
    ranking = Column(Float)
    date_update = Column(DateTime)
    description_app = Column(String)
    times_used = Column(Integer)

    def __init__(self, name_app, ranking, date_update, description_app):
        self.name_app = name_app
        self.ranking = ranking
        self.date_update = date_update
        self.description_app = description_app

    @classmethod
    def from_schema(cls, appstore_schema: appstore_schema.AppStoreSchema):
        return cls(appstore_schema.name_app, appstore_schema.ranking, appstore_schema.date_update, appstore_schema.description_app)
