import vkquick as vq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean


Base = declarative_base()


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer)
    text = Column(String)
    done = Column(Boolean, default=False)
    important = Column(Boolean, default=False)

    @classmethod
    def fetch_by_id(cls, owner_id, id_):
        return vq.current.session.query(
            cls
        ).filter_by(id=id_, owner_id=owner_id).first()


Base.metadata.create_all(vq.current.engine)

vq.current.Notes = Notes
