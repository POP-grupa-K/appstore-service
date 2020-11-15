from sqlalchemy import Column, Integer, LargeBinary

from run import Base


class ImageModel(Base):
    __tablename__ = 'image'

    id_image = Column('idimage', Integer, primary_key=True)
    img = Column(LargeBinary)
    id_app = Column('idapp', Integer)

    def __init__(self, img, id_app):
        self.img = img
        self.id_app = id_app
