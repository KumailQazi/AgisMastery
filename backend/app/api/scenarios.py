from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.base import get_db
from app.models.scenario import Scenario
from app.models.decision_branch import DecisionBranch
from app.models.mastery import MasteryProgress
from app.models.interaction import LearnerInteraction
from app.schemas.scenario import ScenarioRead, ScenarioCreate
from app.telemetry.capture import telemetry
from app.agents.socratic_orchestrator import (
    analyze_scenario,
    generate_socratic_prompt,
    evaluate_mastery,
    adapt_next_scenario
)

router = APIRouter()

class DecisionPayload(BaseModel):
    learner_id: int = 1
    branch_id: int
    time_spent_seconds: float = 12.5
    hints_used: str = ""
    cognitive_load_signal: str = "medium"
    reflection_text: Optional[str] = ""

class ReflectionPayload(BaseModel):
    learner_id: int = 1
    reflection_text: str
    previous_branch_id: int

@router.get("/", response_model=List[ScenarioRead])
def list_scenarios(db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).all()
    results = []
    for s in scenarios:
        branches = db.query(DecisionBranch).filter(DecisionBranch.scenario_id == s.scenario_id).all()
        results.append({
            "scenario_id": s.scenario_id,
            "course_id": s.course_id,
            "context": s.context,
            "decision_point": s.decision_point,
            "scenario_type": s.scenario_type,
            "created_at": s.created_at,
            "branches": branches
        })
    return results

@router.get("/{scenario_id}", response_model=ScenarioRead)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    branches = db.query(DecisionBranch).filter(DecisionBranch.scenario_id == scenario_id).all()
    return {
        "scenario_id": scenario.scenario_id,
        "course_id": scenario.course_id,
        "context": scenario.context,
        "decision_point": scenario.decision_point,
        "scenario_type": scenario.scenario_type,
        "created_at": scenario.created_at,
        "branches": branches
    }

@router.post("/{scenario_id}/decide")
def submit_decision(scenario_id: int, payload: DecisionPayload, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    branch = db.query(DecisionBranch).filter(
        DecisionBranch.branch_id == payload.branch_id,
        DecisionBranch.scenario_id == scenario_id
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Decision branch not found")
    
    accuracy = 1 if branch.is_optimal else 0
    
    # 1. Log silent telemetry
    interaction = telemetry.log_interaction({
        "learner_id": payload.learner_id,
        "scenario_id": scenario_id,
        "branch_chosen": branch.branch_id,
        "accuracy": accuracy,
        "time_spent_seconds": payload.time_spent_seconds,
        "hints_used": payload.hints_used,
        "cognitive_load_signal": payload.cognitive_load_signal,
        "reflection_text": payload.reflection_text,
        "reflective_writing_score": 85.0 if payload.reflection_text else None
    })
    
    # 2. Update mastery state (4/5 rule)
    progress = telemetry.update_mastery(payload.learner_id, scenario_id, accuracy)
    
    # 3. Invoke Socratic Orchestrator Agent logic
    scaffolding = analyze_scenario(scenario.context, f"Attempts: {progress.attempts}, SuccessRate: {progress.success_rate}")
    socratic_res = generate_socratic_prompt(
        scenario_context=scenario.context,
        learner_choice=branch.choice_text,
        is_optimal=branch.is_optimal,
        reflection=payload.reflection_text or ""
    )
    mastery_eval = evaluate_mastery(progress.attempts, int(progress.attempts * float(progress.success_rate or 0)))
    next_adapt = adapt_next_scenario(current_difficulty=2, success_rate=float(progress.success_rate or 0))
    
    return {
        "consequence": branch.consequence,
        "is_optimal": branch.is_optimal,
        "socratic_prompt": socratic_res["prompt"],
        "target_concept": socratic_res.get("target_concept", "decision_making"),
        "scaffolding": scaffolding,
        "mastery_status": {
            "attempts": progress.attempts,
            "success_rate": float(progress.success_rate or 0.0),
            "mastery_achieved": mastery_eval["mastery_achieved"],
            "mastery_achieved_at": progress.mastery_achieved_at
        },
        "next_adaptation": next_adapt
    }

@router.post("/{scenario_id}/reflect")
def submit_reflection(scenario_id: int, payload: ReflectionPayload, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    branch = db.query(DecisionBranch).filter(
        DecisionBranch.branch_id == payload.previous_branch_id
    ).first()
    choice_text = branch.choice_text if branch else "your decision"
    
    # Socratic follow-up coaching
    feedback = (
        f"Insightful reflection on choosing '{choice_text}'. "
        f"You highlighted key trade-offs in high-stakes environments. "
        f"How would you train a junior colleague to recognize these warning signs early?"
    )
    
    return {
        "status": "reflection_recorded",
        "socratic_feedback": feedback,
        "concept_reinforced": "Proactive Risk Communication",
        "ready_for_next_scenario": True
    }
