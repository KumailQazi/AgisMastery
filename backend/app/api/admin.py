from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.models.course import Course
from app.models.scenario import Scenario
from app.models.interaction import LearnerInteraction

router = APIRouter()

@router.get("/system-overview")
def get_system_overview(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    courses_count = db.query(Course).count()
    scenarios_count = db.query(Scenario).count()
    interactions_count = db.query(LearnerInteraction).count()

    return {
        "status": "online",
        "total_users": users_count,
        "total_courses": courses_count,
        "total_scenarios": scenarios_count,
        "total_interactions_logged": interactions_count,
        "adk_orchestrator": "active",
        "model_armor": "active",
        "cloud_run_region": "us-central1"
    }
