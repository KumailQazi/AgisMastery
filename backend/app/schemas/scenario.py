from pydantic import BaseModel
from typing import List
from datetime import datetime

class DecisionBranchCreate(BaseModel):
    choice_text: str
    consequence: str
    is_optimal: bool = False
    socratic_prompt: str = ""

class ScenarioCreate(BaseModel):
    course_id: int
    context: str
    decision_point: str
    scenario_type: str = "general"
    branches: List[DecisionBranchCreate]

class DecisionBranchRead(DecisionBranchCreate):
    branch_id: int
    scenario_id: int
    class Config:
        from_attributes = True

class ScenarioRead(ScenarioCreate):
    scenario_id: int
    created_at: datetime
    branches: List[DecisionBranchRead]
    class Config:
        from_attributes = True
