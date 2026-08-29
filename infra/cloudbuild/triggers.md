# 🛠️ Google Cloud Build Triggers Setup Guide

This guide walks you through setting up automated GitHub CI/CD deployments to Google Cloud Run using Google Cloud Build.

---

## 1. Enable Required GCP APIs
```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com
```

---

## 2. Create Artifact Registry Docker Repository
```bash
gcloud artifacts repositories create mastery-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for Mastery backend & relay services"
```

---

## 3. Configure IAM Permissions for Cloud Build
Grant Cloud Build service account permissions to deploy to Cloud Run:
```bash
PROJECT_NUM=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")

gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:${PROJECT_NUM}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud iam service-accounts add-iam-policy-binding \
  ${PROJECT_NUM}-compute@developer.gserviceaccount.com \
  --member="serviceAccount:${PROJECT_NUM}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

---

## 4. Connect GitHub Repository & Create Build Trigger
1. In the Google Cloud Console, navigate to **Cloud Build > Triggers**.
2. Click **Manage Repositories** and connect your GitHub repo.
3. Click **Create Trigger**:
   * **Name:** `deploy-mastery-main`
   * **Event:** Push to branch
   * **Branch:** `^main$`
   * **Configuration:** Cloud Build configuration file (yaml or json)
   * **Location:** `infra/cloudbuild/cloudbuild.yaml`
4. Click **Create**. Every push to `main` will now automatically build, test, and deploy both Cloud Run services!
