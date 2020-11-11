from sqlalchemy import String, Column, DateTime, Integer, ForeignKey, Float

from appstore.schema import rating_schema
from run import Base


class RatingModel(Base):
    __tablename__ = 'rating'

    id_rating = Column('idrating', Integer, primary_key=True)
    value = Column(Float)
    comm = Column(String)
    id_app = Column('idapp', ForeignKey('appstore.idapp'))

    def __init__(self, value, comm, id_app):
        self.value = value
        self.comm = comm
        self.id_app = id_app

    @classmethod
    def from_schema(cls, rating_schema: rating_schema.RatingSchema):
        return cls(rating_schema.value, rating_schema.comm, rating_schema.id_app)
