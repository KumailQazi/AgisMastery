from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from pydantic import BaseModel

from app.db.base import get_db
from app.models.scenario import Scenario
from app.models.decision_branch import DecisionBranch
from app.telemetry.capture import telemetry
from app.agents.socratic_orchestrator import (
    analyze_scenario,
    generate_socratic_prompt,
    evaluate_mastery,
    adapt_next_scenario
)
from app.core.model_armor import model_armor

router = APIRouter()

class ArmoredDecisionPayload(BaseModel):
    learner_id: int = 1
    branch_id: int
    time_spent_seconds: float = 12.5
    hints_used: str = ""
    cognitive_load_signal: str = "medium"
    reflection_text: Optional[str] = ""

@router.post("/{scenario_id}/decide-safe")
def submit_decision_with_armor(
    scenario_id: int,
    payload: ArmoredDecisionPayload,
    db: Session = Depends(get_db)
):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    branch = db.query(DecisionBranch).filter(
        DecisionBranch.branch_id == payload.branch_id,
        DecisionBranch.scenario_id == scenario_id
    ).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Decision branch not found")

    # 1. Model Armor PII Sanitization
    raw_payload_dict = payload.model_dump()
    sanitized_payload, audit_log = model_armor.sanitize_dict(raw_payload_dict)

    accuracy = 1 if branch.is_optimal else 0

    # 2. Log Silent Telemetry (Safe from PII leaks)
    interaction = telemetry.log_interaction({
        "learner_id": sanitized_payload["learner_id"],
        "scenario_id": scenario_id,
        "branch_chosen": branch.branch_id,
        "accuracy": accuracy,
        "time_spent_seconds": sanitized_payload["time_spent_seconds"],
        "hints_used": sanitized_payload["hints_used"],
        "cognitive_load_signal": sanitized_payload["cognitive_load_signal"],
        "reflection_text": sanitized_payload["reflection_text"],
        "reflective_writing_score": 88.0 if sanitized_payload["reflection_text"] else None
    })

    # 3. Update Mastery State (4/5 Rule)
    progress = telemetry.update_mastery(sanitized_payload["learner_id"], scenario_id, accuracy)

    # 4. Invoke Google ADK Socratic Agent with sanitized reflection
    scaffolding = analyze_scenario(scenario.context, f"Attempts: {progress.attempts}")
    socratic_res = generate_socratic_prompt(
        scenario_context=scenario.context,
        learner_choice=branch.choice_text,
        is_optimal=branch.is_optimal,
        reflection=sanitized_payload.get("reflection_text", "")
    )
    mastery_eval = evaluate_mastery(progress.attempts, int(progress.attempts * float(progress.success_rate or 0)))
    next_adapt = adapt_next_scenario(current_difficulty=2, success_rate=float(progress.success_rate or 0))

    return {
        "consequence": branch.consequence,
        "is_optimal": branch.is_optimal,
        "socratic_prompt": socratic_res["prompt"],
        "sanitization_audit": {
            "pii_redacted": bool(audit_log),
            "redacted_fields": audit_log,
            "armor_status": "active"
        },
        "mastery_status": {
            "attempts": progress.attempts,
            "success_rate": float(progress.success_rate or 0.0),
            "mastery_achieved": mastery_eval["mastery_achieved"]
        },
        "next_adaptation": next_adapt
    }
