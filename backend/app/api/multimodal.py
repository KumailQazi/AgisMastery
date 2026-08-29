from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio

from app.services.gemma_service import gemma_service
from app.services.veo_service import veo_service
from app.services.lyria_service import lyria_service

router = APIRouter()

class EnhancedSocraticRequest(BaseModel):
    scenario_context: str
    learner_choice: str
    is_optimal: bool
    reflection: Optional[str] = ""
    cognitive_load: Optional[str] = "medium"

class VisualizeScenarioRequest(BaseModel):
    scenario_description: str

class ConceptVideoRequest(BaseModel):
    concept_name: str
    struggle_reason: str

class ReflectionAudioRequest(BaseModel):
    feedback_text: str

class PodcastSummaryRequest(BaseModel):
    learner_id: int
    week_number: Optional[int] = 1

@router.post("/socratic-enhanced")
async def socratic_enhanced(payload: EnhancedSocraticRequest):
    """
    Executes Gemma (local Socratic generation), Veo (scenario visualization),
    and Lyria (adaptive audio feedback) concurrently using asyncio.gather().
    """
    gemma_task = gemma_service.generate_socratic_prompt(
        scenario_context=payload.scenario_context,
        learner_choice=payload.learner_choice,
        is_optimal=payload.is_optimal,
        reflection=payload.reflection
    )
    veo_task = veo_service.generate_scenario_visualization(payload.scenario_context)
    lyria_task = lyria_service.generate_flow_state_audio(payload.cognitive_load)

    gemma_res, veo_res, lyria_res = await asyncio.gather(gemma_task, veo_task, lyria_task)

    # Generate spoken audio for the Socratic prompt
    socratic_audio = await lyria_service.generate_socratic_audio(
        socratic_prompt=gemma_res["socratic_prompt"],
        cognitive_load=payload.cognitive_load
    )

    return {
        "socratic_prompt": gemma_res["socratic_prompt"],
        "gemma_privacy_metadata": {
            "model": gemma_res["model"],
            "privacy_mode": gemma_res["privacy_mode"],
            "execution": gemma_res["execution"]
        },
        "veo_visualization": veo_res,
        "lyria_audio_coaching": {
            "socratic_audio_url": socratic_audio["audio_url"],
            "voice_profile": socratic_audio["voice_profile"],
            "ambient_soundscape": lyria_res
        }
    }

@router.post("/visualize-scenario")
async def visualize_scenario(payload: VisualizeScenarioRequest):
    return await veo_service.generate_scenario_visualization(payload.scenario_description)

@router.post("/concept-video")
async def concept_video(payload: ConceptVideoRequest):
    return await veo_service.generate_concept_explanation_video(
        concept_name=payload.concept_name,
        struggle_reason=payload.struggle_reason
    )

@router.post("/reflection-audio")
async def reflection_audio(payload: ReflectionAudioRequest):
    return await lyria_service.narrate_reflection_feedback(payload.feedback_text)

@router.post("/podcast-summary")
async def podcast_summary(payload: PodcastSummaryRequest):
    return await lyria_service.generate_podcast_summary(
        learner_id=payload.learner_id,
        week_number=payload.week_number
    )

@router.get("/models/status")
async def check_models_status():
    gemma_health = await gemma_service.check_health()
    return {
        "status": "active",
        "multimodal_suite": {
            "gemini_core": {"status": "available", "model": "gemini-3.5-pro / gemini-2.0-flash"},
            "gemma_privacy": gemma_health,
            "veo_video": {"status": "available", "model": "veo-2.0-generate"},
            "lyria_audio": {"status": "available", "model": "lyria-tts-v2"}
        }
    }
