variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
  default     = "agentic-hackathon-2026"
}

variable "region" {
  description = "Google Cloud Region for resources"
  type        = string
  default     = "us-central1"
}

variable "db_password" {
  description = "PostgreSQL DB password"
  type        = string
  sensitive   = true
  default     = "MasterySecretPass2026!"
}

variable "gemini_api_key" {
  description = "Gemini API key for ADK agents"
  type        = string
  sensitive   = true
  default     = ""
}
