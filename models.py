from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import JSON

from database import Base


class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    filename = Column(String, index=True)
    raw_data = Column(JSON)
    meta = Column(JSON)