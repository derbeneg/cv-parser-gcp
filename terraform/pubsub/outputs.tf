# terraform/pubsub/outputs.tf
output "topic_name" {
  description = "Name of the Pub/Sub topic for parsed CV messages"
  value       = google_pubsub_topic.parse_topic.name
}