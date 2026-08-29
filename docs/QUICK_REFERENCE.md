# ⚡ Mastery Platform: Quick Reference Guide

> Project: **Mastery — Socratic Scaffolding + Telemetry Learning Platform**  
> Event: **Google All Things Agentic Hackathon 2026** (Collaborative Partner & Startup Excellence Tracks)  
> Stack: **Gemini 3.5**, **Google ADK**, **Gemma**, **Veo**, **Lyria**, **Cloud Run**, **Firestore**, **PostgreSQL**

---

## 🌐 Running Services & URLs

| Component | Port / URL | Description |
|---|---|---|
| **🎨 Web Application** | **[http://localhost:3000](http://localhost:3000)** | Scenario Player, Socratic Dialogue Feed, Silent Telemetry Inspector & Creator Dashboard |
| **🧠 Core Backend API** | **[http://localhost:8000](http://localhost:8000)** | FastAPI Core Backend with Google ADK Socratic Orchestrator |
| **📖 Interactive API Docs** | **[http://localhost:8000/docs](http://localhost:8000/docs)** | Swagger OpenAPI interactive testing playground |
| **⚡ WebSocket Session Relay** | **[http://localhost:8080](http://localhost:8080)** | Real-time WebSocket relay for bi-directional live session streaming (`/ws/{session_id}`) |
| **🩺 Core Health Check** | **[http://localhost:8000/health](http://localhost:8000/health)** | Returns status of Gemini, ADK, Model Armor, and Telemetry Engine |

---

## 📁 Key File Map

### 1. Backend & AI Agents (`mastery-starter/backend/`)
* **[`app/main.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/main.py)**: FastAPI entry point with CORS, routers, and auto-seeding.
* **[`app/agents/socratic_orchestrator.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/agents/socratic_orchestrator.py)**: Google ADK 4-phase `SequentialAgent` pipeline (`LlmAgent` + `FunctionTool`).
* **[`app/core/model_armor.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/core/model_armor.py)**: Google Model Armor PII sanitizer (redacts emails, phone numbers, SSNs, credit cards).
* **[`app/services/`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/services/)**:
  * `gemma_service.py` ➔ On-prem local Socratic tutoring via Ollama.
  * `veo_service.py` ➔ 8-second cinematic scenario video generation & 3D crisis animations.
  * `lyria_service.py` ➔ Cognitive load-adaptive voice coaching & ambient soundscapes.
* **[`app/telemetry/capture.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/telemetry/capture.py)** & **[`app/telemetry/aggregator.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/app/telemetry/aggregator.py)**: Silent struggle detection, hesitation logging, and struggle heatmaps.
* **[`relay/main.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/relay/main.py)**: WebSocket session relay with Redis state management and TTL caching.
* **[`test_e2e_full.py`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/backend/test_e2e_full.py)**: 6-stage automated full-stack verification script.

### 2. Frontend Web App (`mastery-starter/frontend/`)
* **[`index.html`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/frontend/index.html)** & **[`app.js`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/frontend/app.js)**: Standalone web interface with live Socratic dialogue, hesitation timer, and struggle heatmaps.
* **[`src/hooks/useWebSocket.js`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/frontend/src/hooks/useWebSocket.js)**: React hook for WebSocket session state and auto-reconnect.
* **[`src/components/ScenarioPlayer.jsx`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/frontend/src/components/ScenarioPlayer.jsx)**: Live scenario decision player with dual-channel WebSocket + REST execution.
* **[`src/components/TelemetryDashboard.jsx`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/frontend/src/components/TelemetryDashboard.jsx)**: Creator analytics dashboard with Recharts visualizations.

### 3. Infrastructure & CI/CD (`mastery-starter/infra/`)
* **[`terraform/main.tf`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/infra/terraform/main.tf)**: Single-command IaC provisioning Cloud Run, Cloud SQL (PostgreSQL), Firestore, and Secret Manager.
* **[`cloudbuild/cloudbuild.yaml`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/infra/cloudbuild/cloudbuild.yaml)**: 5-step automated build, push, and deployment CI/CD pipeline.

### 4. Hackathon Submission & Specs (`mastery-starter/docs/`)
* **[`HACKATHON_SUBMISSION.md`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/docs/HACKATHON_SUBMISSION.md)**: Devpost submission text with a 4-minute demo video script & timestamp breakdown.
* **[`STARTUP_EXCELLENCE.md`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/docs/STARTUP_EXCELLENCE.md)**: Complete business plan, TAM analysis, GTM roadmap, and pre-seed funding ask.
* **[`EXTRA_MODELS_INTEGRATION.md`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/docs/EXTRA_MODELS_INTEGRATION.md)**: Multimodal learning loop specifications for Gemma, Veo, and Lyria bonus points.
* **[`architecture.md`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/docs/architecture.md)** & **[`architecture.mmd`](file:///Users/mac/Desktop/AgenticHackathon/mastery-starter/docs/architecture.mmd)**: Mermaid system diagrams.

---

## 🛠️ CLI Quick Commands

### Run Full Stack Test (5 Seconds):
```bash
cd mastery-starter/backend
python3 test_e2e_full.py
```

### Test Model Armor PII Redaction:
```bash
curl -X POST http://localhost:8000/api/decisions-armored/1/decide-safe \
  -H "Content-Type: application/json" \
  -d '{
    "learner_id": 1,
    "branch_id": 2,
    "time_spent_seconds": 12.0,
    "reflection_text": "My manager john.doe@acme.com approved this, reach him at 555-123-4567, SSN 000-11-2222"
  }'
```

### Test Multimodal Suite (Gemma + Veo + Lyria):
```bash
curl -X POST http://localhost:8000/api/multimodal/socratic-enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_context": "10 minutes before product launch client demands security check override.",
    "learner_choice": "Refused override and escalated to Incident Commander.",
    "is_optimal": true,
    "reflection": "Zero-trust protocols prevent public data breaches.",
    "cognitive_load": "medium"
  }'
```

### Deploy Entire Stack to Google Cloud Run:
```bash
cd mastery-starter/infra/terraform
terraform init
terraform apply -var="project_id=YOUR_GCP_PROJECT_ID" -var="gemini_api_key=YOUR_GEMINI_KEY"
```
