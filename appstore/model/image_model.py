from sqlalchemy import Column, Integer, LargeBinary, String

from run import Base


class ImageModel(Base):
    __tablename__ = 'image'

    id_image = Column('idimage', Integer, primary_key=True)
    img = Column('img', LargeBinary)
    filename = Column('filename', String)
    id_app = Column('idapp', Integer)

    def __init__(self, img, filename, id_app):
        self.img = img
        self.filename = filename
        self.id_app = id_app
