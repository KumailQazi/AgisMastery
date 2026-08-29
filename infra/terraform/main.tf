terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Required Google Cloud APIs
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "firestore.googleapis.com",
    "secretmanager.googleapis.com",
    "aiplatform.googleapis.com",
    "cloudbuild.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

# 2. Secret Manager for Gemini API Key
resource "google_secret_manager_secret" "gemini_key_secret" {
  secret_id = "gemini-api-key"
  replication {
    auto {}
  }
  depends_on = [google_project_service.enabled_apis]
}

resource "google_secret_manager_secret_version" "gemini_key_version" {
  secret      = google_secret_manager_secret.gemini_key_secret.id
  secret_data = var.gemini_api_key != "" ? var.gemini_api_key : "dummy-gemini-key"
}

# 3. Google Cloud Firestore Database (Telemetry & Resumable Session State)
resource "google_firestore_database" "mastery_firestore" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  depends_on  = [google_project_service.enabled_apis]
}

# 4. Google Cloud SQL (PostgreSQL 15 for Relational Mastery Data)
resource "google_sql_database_instance" "mastery_postgres" {
  name             = "mastery-postgres-instance"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro" # Cost-effective for Hackathon Demo
    ip_configuration {
      ipv4_enabled = true
    }
  }
  deletion_protection = false
  depends_on          = [google_project_service.enabled_apis]
}

resource "google_sql_database" "mastery_db" {
  name     = "mastery_db"
  instance = google_sql_database_instance.mastery_postgres.name
}

resource "google_sql_user" "mastery_db_user" {
  name     = "mastery_user"
  instance = google_sql_database_instance.mastery_postgres.name
  password = var.db_password
}

# 5. Google Cloud Run (Mastery FastAPI & ADK Socratic Orchestrator Backend)
resource "google_cloud_run_v2_service" "mastery_api" {
  name     = "mastery-api-service"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/mastery-backend:latest"
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
      env {
        name  = "APP_ENV"
        value = "production"
      }
      env {
        name  = "DATABASE_URL"
        value = "postgresql+psycopg2://mastery_user:${var.db_password}@${google_sql_database_instance.mastery_postgres.public_ip_address}:5432/mastery_db"
      }
      env {
        name  = "USE_FIRESTORE"
        value = "true"
      }
      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_key_secret.secret_id
            version = "latest"
          }
        }
      }
    }
  }
  depends_on = [
    google_project_service.enabled_apis,
    google_sql_database.mastery_db,
    google_firestore_database.mastery_firestore
  ]
}

# Allow public unauthenticated access to Cloud Run for Hackathon Demo
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.mastery_api.name
  location = google_cloud_run_v2_service.mastery_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
