from sqlalchemy import Column, Integer, String, Text
from database import Base

class ProjectRequest(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="Pending")
