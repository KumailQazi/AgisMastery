# 🏛️ Mastery Architecture & Technical Specifications

Mastery is an autonomous agentic learning platform built with **Gemini 3.5**, **Google ADK (Agent Development Kit)**, and **Google Cloud Platform**. It is specifically designed to eliminate the 35.8% gap between course completion and real-world decision mastery.

---

## 1. System Context Diagram (Level 1)

```mermaid
flowchart TD
    subgraph Users ["Actors & Stakeholders"]
        Learner["👤 Learner / Employee<br/>(Practices High-Stakes Decisions)"]
        Creator["👩‍🏫 Course Creator / L&D Lead<br/>(Designs Scenarios & Reviews Heatmaps)"]
        Admin["🛡️ Enterprise Admin<br/>(Security & Compliance Governance)"]
    end

    subgraph Platform ["Mastery AI Platform"]
        MasterySystem["⚡ Mastery System<br/>(FastAPI + Google ADK + Gemini 3.5)"]
    end

    subgraph ExternalServices ["External & Cloud Ecosystem"]
        GCP["☁️ Google Cloud Platform<br/>(Cloud Run, Cloud SQL, Firestore)"]
        GeminiAPI["🤖 Google Gemini API<br/>(gemini-2.0-flash / gemini-3.5)"]
        LMS["🎓 Enterprise LMS / HRIS<br/>(SCORM / xAPI / Webhooks)"]
    end

    Learner -->|Solves scenarios & Reflects| MasterySystem
    Creator -->|Builds scenarios & inspects telemetry| MasterySystem
    Admin -->|Audits zero-trust compliance| MasterySystem

    MasterySystem -->|Runs containerized workloads| GCP
    MasterySystem -->|Executes Socratic reasoning| GeminiAPI
    MasterySystem -->|Syncs mastery grades| LMS
```

---

## 2. Container Diagram (Level 2)

```mermaid
flowchart TD
    subgraph ClientLayer ["Client Layer"]
        SPA["🌐 React 18 + Vite Web App<br/>• Scenario Player<br/>• Socratic Dialogue Feed<br/>• Creator Heatmap Dashboard"]
    end

    subgraph ComputeLayer ["Compute Layer (Google Cloud Run)"]
        FastAPI["🚀 FastAPI Backend Service<br/>• JWT Authentication<br/>• REST & SSE Endpoints<br/>• Silent Telemetry Capture Engine"]
        ADK["🧠 Google ADK Agent Runtime<br/>• SequentialAgent Pipeline<br/>• Socratic Dialogue Orchestrator"]
    end

    subgraph StorageLayer ["Storage & State Layer (Google Cloud)"]
        CloudSQL[("🐘 Google Cloud SQL (PostgreSQL)<br/>• Users & Roles<br/>• Scenarios & Branches<br/>• Mastery Progress (4/5 Rule)")]
        Firestore[("🔥 Google Cloud Firestore<br/>• Silent Telemetry Events<br/>• Resumable Session State<br/>• Cognitive Load Signals")]
        RedisStore[("⚡ Redis Cache & Broker<br/>• Fast Session Token Cache<br/>• Celery Task Queue")]
        SecretMgr["🔐 Google Secret Manager<br/>• Gemini API Keys<br/>• JWT Secrets"]
    end

    SPA -->|HTTPS / REST| FastAPI
    FastAPI -->|Executes Agent Pipeline| ADK
    ADK -->|Function Tools & Prompts| Gemini["🤖 Google Gemini 3.5 / 2.0 Flash"]
    FastAPI -->|CRUD & Relations| CloudSQL
    FastAPI -->|Stream Telemetry Events| Firestore
    FastAPI -->|Pub/Sub Caching| RedisStore
    FastAPI -->|Fetch Credentials| SecretMgr
```

---

## 3. Google ADK Socratic Agent Flow Diagram (Level 3)

The **Socratic Orchestrator** is implemented as a `google.adk.agents.SequentialAgent` executing 4 coordinated phases:

```mermaid
sequenceDiagram
    autonumber
    actor Learner as 👤 Learner
    participant API as 🚀 FastAPI API
    participant Telemetry as 📡 Telemetry Engine
    participant SA as 🔍 Scenario Analyzer (LlmAgent)
    participant SG as 💬 Socratic Generator (LlmAgent)
    participant ME as 🏆 Mastery Evaluator (LlmAgent)
    participant DA as 🔄 Difficulty Adapter (LlmAgent)
    participant DB as 🐘 Cloud SQL / Firestore

    Learner->>API: Submits Decision (Branch #, Time Spent, Hesitation)
    API->>Telemetry: Log Silent Interaction & Cognitive Load Signals
    Telemetry->>DB: Store Interaction & Update Attempts Counter

    API->>SA: [Phase I] Analyze scenario context & history
    SA-->>API: Return Scaffolding Level (1 to 4) + Rationale

    API->>SG: [Phase II] Generate Socratic Follow-up Prompt
    Note over SG: Formulates question targeting underlying trade-off (Never gives answer)
    SG-->>API: Return Socratic Prompt & Target Concept

    API->>ME: [Phase III] Evaluate Mastery State
    Note over ME: Applies 4/5 accurate decisions rule across variations
    ME-->>API: Return Mastery Status (Achieved / In Progress)

    API->>DA: [Phase IV] Adapt Next Scenario Difficulty
    DA-->>API: Return Next Difficulty Level (1 to 5)

    API-->>Learner: Consequence + Socratic Prompt + Updated Mastery Progress
    Learner->>API: Submits Socratic Reflection
    API-->>Learner: Socratic Confirmation & Advance to Adapted Scenario
```

---

## 4. Silent Telemetry & Redesign Dataflow

```mermaid
flowchart LR
    subgraph TelemetryCapture ["Silent Telemetry Capture"]
        T1["⏱ Time-per-Decision Tracker"]
        T2["💡 Scaffolding Hint Clicks"]
        T3["⏸ Hesitation & Pause Points"]
        T4["✍️ Reflection Writing Sentiment"]
    end

    subgraph Processing ["Telemetry Ingestion Engine"]
        Engine["📡 Telemetry Aggregator<br/>(app/telemetry/capture.py)"]
    end

    subgraph AnalyticsDashboard ["Creator Dashboard & Heatmap"]
        D1["🔥 Cognitive Load Heatmap<br/>(Identifies Scenario Bottlenecks)"]
        D2["📉 35.8% Mastery Gap Visualization"]
        D3["🛠 Automated Course Redesign Insights"]
    end

    T1 --> Engine
    T2 --> Engine
    T3 --> Engine
    T4 --> Engine

    Engine --> D1
    Engine --> D2
    Engine --> D3
```
