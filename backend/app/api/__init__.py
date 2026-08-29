from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.scenarios import router as scenarios_router
from app.api.decisions import router as decisions_router
from app.api.decisions_with_armor import router as armored_decisions_router
from app.api.telemetry import router as telemetry_router
from app.api.admin import router as admin_router
from app.api.multimodal import router as multimodal_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(scenarios_router, prefix="/scenarios", tags=["Scenarios & Socratic Agent"])
api_router.include_router(decisions_router, prefix="/decisions", tags=["Decisions"])
api_router.include_router(armored_decisions_router, prefix="/decisions-armored", tags=["Model Armor Decisions"])
api_router.include_router(telemetry_router, prefix="/telemetry", tags=["Telemetry & Analytics"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin & Governance"])
api_router.include_router(multimodal_router, prefix="/multimodal", tags=["Extra Google Models (Gemma, Veo, Lyria)"])
