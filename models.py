
from sqlalchemy import Column, Integer, String

from .database import Base

class URLModel(Base):
    __tablename__ = "short_url"
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    long_url = Column(String,index=True,nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=True)

