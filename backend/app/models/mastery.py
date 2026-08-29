from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class MasteryProgress(Base):
    __tablename__ = "mastery_progress"
    progress_id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    attempts = Column(Integer, default=0)
    success_rate = Column(Numeric(5, 2), default=0.0)
    last_practiced_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    mastery_achieved_at = Column(DateTime(timezone=True), nullable=True)
