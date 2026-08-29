from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    scenario_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    context = Column(Text, nullable=False)
    decision_point = Column(Text, nullable=False)
    scenario_type = Column(String, default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
