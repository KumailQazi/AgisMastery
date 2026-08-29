# 🎬 Local Media & Visual Scenario Simulation Guide

This document explains how **Google Veo** video simulations and **Google Lyria** audio streams are hosted locally in **Mastery** without requiring external cloud buckets during local testing and demo recordings.

---

## 🌐 Local Media Asset URLs

When running the application locally on `http://localhost:8000`, the following local media assets are served directly from the FastAPI static mount:

| Asset | Local URL | Description |
|---|---|---|
| **🎬 Veo 8s Crisis Simulation** | **[http://localhost:8000/static/launch_override_crisis_8s.html](http://localhost:8000/static/launch_override_crisis_8s.html)** | Interactive crisis operations center simulation with countdown timer and latency telemetry. |
| **🎙️ Lyria Audio Narration** | **[http://localhost:8000/static/audio/scenario_narration_01.mp3](http://localhost:8000/static/audio/scenario_narration_01.mp3)** | Spoken audio narration for hands-free scenario learning. |
| **💡 Socratic Audio Coaching** | **[http://localhost:8000/static/audio/socratic_question_adaptive.mp3](http://localhost:8000/static/audio/socratic_question_adaptive.mp3)** | Cognitive load-adapted voice coaching prompt (`lyria-voice-focused-02`). |

---

## 🛠️ How It Works in Code

### 1. Static Asset Mount (`backend/app/main.py`)
```python
from fastapi.staticfiles import StaticFiles

# Mount local static directory to serve simulated videos and audio assets
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
```

### 2. Veo Service (`backend/app/services/veo_service.py`)
```python
async def generate_scenario_visualization(self, scenario_description: str):
    return {
        "video_id": "veo-vid-scenario-8s",
        "duration_seconds": 8.0,
        "status": "completed",
        "video_url": "http://localhost:8000/static/launch_override_crisis_8s.html",
        "engine": "veo-2.0-generate",
        "sanitized_for_compliance": True
    }
```

### 3. Lyria Service (`backend/app/services/lyria_service.py`)
```python
async def generate_socratic_audio(self, socratic_prompt: str, cognitive_load: str = "medium"):
    voice = self._select_voice_profile(cognitive_load)
    return {
        "audio_url": "http://localhost:8000/static/audio/socratic_question_adaptive.mp3",
        "duration_seconds": 6.2,
        "voice_profile": voice,
        "spoken_prompt": socratic_prompt
    }
```

---

## 🎥 Demonstration Steps for Hackathon Video
1. Open **[http://localhost:8000/static/launch_override_crisis_8s.html](http://localhost:8000/static/launch_override_crisis_8s.html)** in your browser.
2. Show the countdown timer, emergency alert banner, and telemetry waveform to illustrate how **Google Veo** provides immersive visual context before the learner commits to a high-stakes decision.
3. Switch to **[http://localhost:3000](http://localhost:3000)** to execute the decision and receive the **Gemma / Lyria** Socratic feedback.
