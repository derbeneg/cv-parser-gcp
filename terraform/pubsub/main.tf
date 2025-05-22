# terraform/pubsub/main.tf
resource "google_pubsub_topic" "parse_topic" {
  name = "cv-parse-topic"
}

resource "google_pubsub_subscription" "worker_sub" {
  name                 = "cv-parse-sub"
  topic                = google_pubsub_topic.parse_topic.name
  ack_deadline_seconds = 30
}