from sqlalchemy import String, Column, DateTime, Integer

from appstore.schema import appstore
from run import Base


class AppStore(Base):
    __tablename__ = 'appstore'

    id_app = Column('idapp', Integer, primary_key=True)
    name_app = Column(String)
    ranking = Column(Integer)
    date_update = Column(DateTime)
    description_app = Column(String)

    @classmethod
    def from_schema(cls, appstore_schema: appstore.AppStore):
        cls.name_app = appstore_schema.name_app
        cls.ranking = appstore_schema.ranking
        cls.date_update = appstore_schema.date_update
        cls.description_app = appstore_schema.description_app
        return cls()
