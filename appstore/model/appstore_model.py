from sqlalchemy import String, Column, DateTime, Integer, Float
from sqlalchemy.orm import relationship

from appstore.schema import appstore_schema
from appstore.utils.db.db_config import Base


class AppStoreModel(Base):
    __tablename__ = 'appstore'

    id_app = Column('idapp', Integer, primary_key=True)
    name_app = Column('name', String)
    ranking = Column('ranking', Float)
    date_update = Column('dateupdate', DateTime)
    description_app = Column('description', String)
    times_used = Column('timesused', Integer)
    ratings = relationship("RatingModel", cascade="all, delete")
    status = Column('statusapp', String)
    id_user = Column('iduser', Integer)

    def __init__(self, name_app, ranking, date_update, description_app, times_used, id_user):
        self.name_app = name_app
        self.ranking = ranking
        self.date_update = date_update
        self.description_app = description_app
        self.times_used = times_used
        self.id_user = id_user

    @classmethod
    def from_schema(cls, appstore_schema: appstore_schema.AppStoreSchema):
        return cls(appstore_schema.name_app, appstore_schema.ranking, appstore_schema.date_update, appstore_schema.description_app, appstore_schema.times_used, appstore_schema.id_user)
