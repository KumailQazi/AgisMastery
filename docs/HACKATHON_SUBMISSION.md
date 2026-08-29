# 🏆 Devpost Hackathon Submission Template

**Project Title:** Mastery: Socratic Scaffolding + Telemetry Learning Platform  
**One-Sentence Tagline:** An autonomous agentic learning platform powered by Gemini 3.5 and Google ADK that bridges the 35.8% gap between course completion and real decision mastery through Socratic dialogue and silent telemetry.  
**Track:** Collaborative Partner *(Secondary: Taskmaster)*  

---

## 🎥 Demo Video (Under 4 Minutes)
* **Link:** `https://youtu.be/YOUR_DEMO_VIDEO_ID` *(Public / Unlisted on YouTube or Vimeo)*
* **Video Script & Timestamp Breakdown:**
  * **0:00 – 0:15:** Immediate hook — The Scenario Decision Player loading a live workplace crisis ("10-Minute Launch Override").
  * **0:15 – 1:30:** The Socratic Dialogue Loop — Learner makes a decision, gets immediate consequence, and is guided by the Gemini Socratic Agent rather than given answers.
  * **1:30 – 2:30:** Live Silent Telemetry — Real-time telemetry inspector demonstrating hesitation tracking, cognitive load signals, and the 4/5 Mastery progress update.
  * **2:30 – 3:30:** Course Creator Dashboard — Visualizing the 35.8% Mastery Gap, struggle heatmaps, and automated redesign insights.
  * **3:30 – 4:00:** Google Cloud Proof — Live Cloud Run console, Vertex AI logs, and Firestore database collections.

---

## 💡 Inspiration
Traditional e-learning is broken: **94.2% of learners complete online courses, yet only 58.4% can make sound decisions under pressure**—leaving a massive 35.8% Mastery Gap. Slide decks and multiple-choice quizzes test rote memory, not decision-making under stress. Furthermore, instructional designers and L&D leaders have zero visibility into *where* learners struggle. We built **Mastery** to replace passive content consumption with Socratic, decision-driven practice.

---

## ⚡ What It Does
* **For Learners:**
  * **Realistic High-Stakes Scenarios:** Engages learners in branching crisis simulations with real downstream consequences.
  * **Socratic AI Guidance:** Powered by Gemini 3.5, the agent never gives the answer away; it asks targeted Socratic questions to scaffold mental models.
  * **Adaptive Scaffolding:** Dynamically adjusts difficulty (Levels 1–5) based on real-time mastery performance (4/5 rule).
* **For Course Creators & L&D Leaders:**
  * **Cognitive Load & Struggle Heatmap:** Passively maps which decision branches cause friction, hesitation, or drop-off.
  * **Mastery vs. Completion Gap Analytics:** Quantifies real competency gain vs. simple completion checkboxes.
  * **Automated Redesign Recommendations:** AI-generated course redesign suggestions based on aggregated learner telemetry.

---

## 🛠️ How We Built It

### Tech Stack Table:
| Layer | Technologies Used |
|---|---|
| **AI Foundation** | Google Gemini 3.5 & `gemini-2.0-flash` via Gemini API / Vertex AI |
| **Agent Framework** | **Google Agent Development Kit (`google-adk`)** using `SequentialAgent` + `LlmAgent` |
| **Backend Compute** | FastAPI, Python 3.11+, Uvicorn, SQLAlchemy |
| **Frontend UI** | React 18, Vite, Tailwind CSS, Recharts, Modern Glassmorphism |
| **Data & State Storage** | Google Cloud SQL (PostgreSQL 16), Google Cloud Firestore (Telemetry/Session State), Redis Memorystore |
| **Infrastructure & IaC** | Google Cloud Run, Google Secret Manager, Terraform (`infra/terraform/`) |

### Google ADK Multi-Phase SequentialAgent Pipeline:
1. **Phase I (Scenario Analyzer):** Evaluates scenario context and prior learner readiness to assign a scaffolding level (1–4).
2. **Phase II (Socratic Generator):** Formulates targeted Socratic follow-up questions targeting underlying trade-offs.
3. **Phase III (Mastery Evaluator):** Enforces the 4/5 decision rule to verify authentic mastery.
4. **Phase IV (Difficulty Adapter):** Calibrates the next scenario difficulty level.

---

## 🚀 How to Run It

### Local Quickstart:
```bash
# 1. Start Backend & Database
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# 2. Start Frontend
cd ../frontend
python3 -m http.server 3000
```

### Google Cloud Terraform Deployment (1 Command):
```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply
```

---

## 🔑 Demo Credentials
* **Creator Portal:** `creator@mastery.ai` / `mastery2026`
* **Learner Portal:** `learner@mastery.ai` / `learner2026`

---

## 🌟 What Makes It Unique (5 Key Differentiators)
1. **Socratic, Not Answer-Giving:** Uses Gemini to cultivate deep reasoning rather than passive text generation.
2. **True Mastery (4/5 Rule):** Demands consistency across varied contexts to pass, not a one-off quiz score.
3. **Silent Cognitive Telemetry:** Captures hesitation, hints, and time without interrupting the learner flow.
4. **100% Google ADK Native:** Built from the ground up on Google's new Agent Development Kit.
5. **Resumable State:** Persistent cross-session state backed by Google Cloud Firestore.

---

## 🗺️ Future Roadmap
* **Multimodal Voice Mode:** Low-latency verbal Socratic coaching using Gemini Live Audio Preview.
* **Scenario A/B Testing Engine:** Automated creator A/B testing with statistical power analysis on mastery outcomes.
* **Enterprise LMS Integration:** LTI 1.3 / xAPI integration with Canvas, Blackboard, and Workday.
* **Model Armor Integration:** Inline enterprise guardrails for prompt safety and PII protection.

---

## 📜 Attribution & Licensing
* **Reference Patterns:** Socratic dialogue scaffolding patterns, telemetry data structures, and dashboard UI references adapted into Google ADK and Gemini architectures.
* **License:** MIT License
