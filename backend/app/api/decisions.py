from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.scenario import Scenario
from app.models.decision_branch import DecisionBranch
from app.schemas.decision import DecisionSubmit, DecisionResult
from app.telemetry.capture import telemetry
from app.agents.socratic_orchestrator import (
    analyze_scenario,
    generate_socratic_prompt,
    evaluate_mastery,
    adapt_next_scenario
)

router = APIRouter()

@router.post("/{scenario_id}", response_model=DecisionResult)
def submit_decision(scenario_id: int, payload: DecisionSubmit, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    branch = db.query(DecisionBranch).filter(
        DecisionBranch.branch_id == payload.decision_branch_id,
        DecisionBranch.scenario_id == scenario_id
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Decision branch not found")

    accuracy = 1 if branch.is_optimal else 0

    # Log telemetry
    telemetry.log_interaction({
        "learner_id": 1,
        "scenario_id": scenario_id,
        "branch_chosen": branch.branch_id,
        "accuracy": accuracy,
        "time_spent_seconds": payload.time_spent,
        "hints_used": payload.hints_used,
        "cognitive_load_signal": payload.cognitive_load_signal,
        "reflection_text": payload.reflection_text
    })

    progress = telemetry.update_mastery(1, scenario_id, accuracy)
    socratic_res = generate_socratic_prompt(
        scenario_context=scenario.context,
        learner_choice=branch.choice_text,
        is_optimal=branch.is_optimal,
        reflection=payload.reflection_text or ""
    )

    return {
        "consequence": branch.consequence,
        "socratic_prompt": socratic_res["prompt"],
        "is_optimal": branch.is_optimal,
        "mastery_progress": {
            "attempts": progress.attempts,
            "success_rate": float(progress.success_rate or 0.0),
            "mastery_achieved": progress.attempts >= 5 and float(progress.success_rate or 0.0) >= 0.8
        }
    }
