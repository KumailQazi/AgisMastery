from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from app.db.base import Base

class DecisionBranch(Base):
    __tablename__ = "decision_branches"
    branch_id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    choice_text = Column(Text, nullable=False)
    consequence = Column(Text, nullable=False)
    is_optimal = Column(Boolean, default=False)
    socratic_prompt = Column(Text)
