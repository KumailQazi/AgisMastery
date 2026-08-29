from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base

class LearnerInteraction(Base):
    __tablename__ = "learner_interactions"
    interaction_id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    branch_chosen = Column(Integer, ForeignKey("decision_branches.branch_id"), nullable=False)
    accuracy = Column(Integer)  # 1 or 0
    time_spent_seconds = Column(Numeric(10, 2))
    hints_used = Column(String)
    cognitive_load_signal = Column(String)
    reflection_text = Column(Text)
    reflective_writing_score = Column(Numeric(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
