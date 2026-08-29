from pydantic import BaseModel
from typing import Optional

class DecisionSubmit(BaseModel):
    decision_branch_id: int
    reflection_text: Optional[str] = None
    time_spent: float = 0.0
    hints_used: str = ""
    cognitive_load_signal: str = ""

class DecisionResult(BaseModel):
    consequence: str
    socratic_prompt: str
    is_optimal: bool
    mastery_progress: dict
