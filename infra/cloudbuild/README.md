# 🚀 Mastery Cloud Build CI/CD Pipeline

This directory contains automated continuous deployment configurations for deploying Mastery to **Google Cloud Run**.

---

## 🏗️ Architecture Flow

```mermaid
flowchart LR
    Dev["💻 Developer Push"] -->|git push main| GitHub["🐙 GitHub Repository"]
    GitHub -->|Webhook Trigger| CloudBuild["⚙️ Google Cloud Build"]
    
    subgraph BuildPush ["Build & Push"]
        CloudBuild -->|Build & Tag| DockerAPI["📦 mastery-api Image"]
        CloudBuild -->|Build & Tag| DockerRelay["📦 mastery-relay Image"]
        DockerAPI -->|Push| AR["🏛️ Google Artifact Registry"]
        DockerRelay -->|Push| AR
    end

    subgraph DeployRun ["Zero-Downtime Deployment"]
        AR -->|Deploy Revision| RunAPI["🚀 Cloud Run (API)"]
        AR -->|Deploy Revision| RunRelay["⚡ Cloud Run (Relay)"]
    end
```

---

## 📂 Directory Contents
* **`cloudbuild.yaml`**: Full 5-step build, push, and deployment pipeline for multi-service Cloud Run.
* **`triggers.md`**: Step-by-step instructions to enable APIs, create Artifact Registry, and link GitHub triggers.
