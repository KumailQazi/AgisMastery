from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="learner")  # learner | creator | admin
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
