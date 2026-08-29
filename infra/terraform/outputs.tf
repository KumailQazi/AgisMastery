output "cloud_run_url" {
  description = "The public URL of the deployed Mastery Cloud Run service"
  value       = google_cloud_run_v2_service.mastery_api.uri
}

output "cloud_sql_ip" {
  description = "Public IP of Cloud SQL PostgreSQL instance"
  value       = google_cloud_sql_database_instance.mastery_postgres.public_ip_address
}

output "firestore_database_name" {
  description = "Name of Firestore Database"
  value       = google_firestore_database.mastery_firestore.name
}

output "secret_manager_gemini_key_id" {
  description = "Secret ID for Gemini API Key"
  value       = google_secret_manager_secret.gemini_key_secret.secret_id
}
