from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.db.base import Base, engine, SessionLocal
from app.api import api_router
from app.models.user import User
from app.models.course import Course
from app.models.scenario import Scenario
from app.models.decision_branch import DecisionBranch
from app.models.organization import Organization
from app.core.security import get_password_hash

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Scenario).first():
            return

        org = Organization(name="Acme Enterprise Tech")
        db.add(org)
        db.commit()
        db.refresh(org)

        admin_user = User(
            email="creator@mastery.ai",
            hashed_password=get_password_hash("mastery2026"),
            role="creator",
            organization_id=org.organization_id
        )
        learner_user = User(
            email="learner@mastery.ai",
            hashed_password=get_password_hash("learner2026"),
            role="learner",
            organization_id=org.organization_id
        )
        db.add_all([admin_user, learner_user])
        db.commit()
        db.refresh(admin_user)
        db.refresh(learner_user)

        course = Course(
            creator_id=admin_user.user_id,
            title="High-Stakes Decision Making & Incident Management",
            description="Master complex real-time decision trade-offs under high cognitive load.",
            mastery_target=80.0
        )
        db.add(course)
        db.commit()
        db.refresh(course)

        # Scenario 1
        s1 = Scenario(
            course_id=course.course_id,
            context="You are 10 minutes before a global product launch. The enterprise client demands an immediate override on a security check to meet their press deadline. Bypassing it violates protocol but ensures an on-time kickoff.",
            decision_point="The client VP is on the emergency line demanding immediate green light. What do you do?",
            scenario_type="critical_incident"
        )
        db.add(s1)
        db.commit()
        db.refresh(s1)

        b1_1 = DecisionBranch(
            scenario_id=s1.scenario_id,
            choice_text="Immediately approve the override to preserve client relationship and hit the press deadline.",
            consequence="The launch happens on time, but 2 hours later an unauthorized vulnerability exposure is detected, causing a security incident report.",
            is_optimal=False,
            socratic_prompt="You prioritized speed over security protocol. What unintended downstream consequences occurred, and what risk threshold should govern overrides?"
        )
        b1_2 = DecisionBranch(
            scenario_id=s1.scenario_id,
            choice_text="Refuse the override, explain the security risk clearly, and escalate immediately to the Incident Commander.",
            consequence="The launch is delayed by 15 minutes, but the critical validation passes cleanly with zero vulnerability leaks.",
            is_optimal=True,
            socratic_prompt="Strong decision. Why did protocol adherence matter more than short-term client pressure in this specific context?"
        )
        b1_3 = DecisionBranch(
            scenario_id=s1.scenario_id,
            choice_text="Quietly run a partial test while telling the client everything is approved.",
            consequence="Communication breakdown occurs; the deployment partially fails mid-stream with inconsistent state across regions.",
            is_optimal=False,
            socratic_prompt="You attempted a middle-ground compromise without full visibility. How does partial disclosure affect team trust during incidents?"
        )
        db.add_all([b1_1, b1_2, b1_3])
        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_database()
    yield

app = FastAPI(
    title="Mastery — Socratic Scaffolding + Telemetry Learning Platform",
    description="Agentic learning system powered by Gemini 3.5, Google ADK, Gemma, Veo, and Lyria.",
    version="0.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mastery-backend",
        "version": "0.2.0",
        "agent": "Google ADK Gemini Socratic Orchestrator",
        "extra_models": ["Gemma", "Veo", "Lyria"],
        "model_armor": "active"
    }

@app.get("/")
def root():
    return {
        "name": "Mastery API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
        "static_assets": "/static"
    }
