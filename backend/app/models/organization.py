from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Organization(Base):
    __tablename__ = "organizations"
    organization_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
