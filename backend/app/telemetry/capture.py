from datetime import datetime
from typing import Dict, Any
from app.db.base import SessionLocal
from app.models.interaction import LearnerInteraction
from app.models.mastery import MasteryProgress
from sqlalchemy.sql import func

class TelemetryCapture:
    def log_interaction(self, payload: Dict[str, Any]) -> LearnerInteraction:
        db = SessionLocal()
        try:
            interaction = LearnerInteraction(
                learner_id=payload["learner_id"],
                scenario_id=payload["scenario_id"],
                branch_chosen=payload["branch_chosen"],
                accuracy=payload.get("accuracy"),
                time_spent_seconds=payload.get("time_spent_seconds"),
                hints_used=payload.get("hints_used", ""),
                cognitive_load_signal=payload.get("cognitive_load_signal", ""),
                reflection_text=payload.get("reflection_text", ""),
                reflective_writing_score=payload.get("reflective_writing_score"),
            )
            db.add(interaction)
            db.commit()
            db.refresh(interaction)
            return interaction
        finally:
            db.close()

    def update_mastery(self, learner_id: int, scenario_id: int, accuracy: int):
        db = SessionLocal()
        try:
            progress = db.query(MasteryProgress).filter_by(
                learner_id=learner_id, scenario_id=scenario_id
            ).first()
            if not progress:
                progress = MasteryProgress(
                    learner_id=learner_id,
                    scenario_id=scenario_id,
                    attempts=0,
                    success_rate=0.0,
                )
                db.add(progress)
            progress.attempts += 1
            interactions = db.query(LearnerInteraction).filter_by(
                learner_id=learner_id, scenario_id=scenario_id
            ).all()
            correct = sum(1 for i in interactions if i.accuracy == 1)
            progress.success_rate = correct / progress.attempts if progress.attempts > 0 else 0.0
            if progress.attempts >= 5 and progress.success_rate >= 0.8 and not progress.mastery_achieved_at:
                progress.mastery_achieved_at = func.now()
            db.commit()
            db.refresh(progress)
            return progress
        finally:
            db.close()

telemetry = TelemetryCapture()
