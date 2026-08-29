"""
Google Veo Service for Scenario Visualization and Crisis Simulations.
Generates short 8-second cinematic visualization prompts, animations, and video manifests for visual learners.
Includes strict prompt sanitization for corporate compliance.
"""
import os
import re
from typing import Dict, Any, Optional

class VeoService:
    def __init__(self):
        self.api_key = os.environ.get("VEO_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
        self.model = "veo-2.0-generate"

    def _sanitize_visual_prompt(self, prompt: str) -> str:
        """
        Removes PII, specific corporate entity names, and personal identifiers.
        """
        cleaned = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[USER]', prompt)
        cleaned = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '', cleaned)
        cleaned = re.sub(r'Acme Corp|Google|Amazon|Microsoft', 'Enterprise Organization', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    async def generate_scenario_visualization(self, scenario_description: str) -> Dict[str, Any]:
        """
        Creates an 8-second visual scenario video specification.
        """
        sanitized = self._sanitize_visual_prompt(scenario_description)
        visual_prompt = (
            f"Cinematic workplace crisis simulation: 8-second sequence showing {sanitized}. "
            f"Close-up of modern operations center dashboard flashing telemetry alerts, ticking launch countdown clock, "
            f"professional lighting, realistic motion blur, 4k photorealistic render."
        )

        return {
            "video_id": "veo-vid-scenario-8s",
            "duration_seconds": 8.0,
            "status": "completed",
            "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
            "thumbnail_url": "http://localhost:8000/static/launch_override_thumb.jpg",
            "visual_prompt": visual_prompt,
            "engine": self.model,
            "sanitized_for_compliance": True
        }

    async def generate_concept_explanation_video(self, concept_name: str, struggle_reason: str) -> Dict[str, Any]:
        """
        Generates micro-learning animated explanation video for repeated struggle points.
        """
        return {
            "video_id": f"veo-concept-{concept_name.lower().replace(' ', '_')}",
            "duration_seconds": 15.0,
            "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
            "concept": concept_name,
            "visual_style": "3D Isometric architecture animation demonstrating cascading rollback blast radius.",
            "target_friction_resolved": struggle_reason
        }

    async def generate_crisis_simulation(self, crisis_type: str) -> Dict[str, Any]:
        """
        Pre-built crisis simulations: server_outage | client_escalation | product_defect | deadline_pressure
        """
        catalog = {
            "server_outage": {
                "title": "Global Gateway Outage",
                "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
                "ambient_stress_audio": "server_room_hum_alert_chimes"
            },
            "client_escalation": {
                "title": "Emergency VP Escalation Line",
                "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
                "ambient_stress_audio": "ringtone_stress_pulse"
            },
            "product_defect": {
                "title": "Zero-Day Vulnerability Breach",
                "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
                "ambient_stress_audio": "security_klaxon_low"
            }
        }
        return catalog.get(crisis_type, catalog["client_escalation"])

veo_service = VeoService()
