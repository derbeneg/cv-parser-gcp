// terraform/function/variables.tf

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region for the function"
  default     = "us-central1"
}

variable "topic" {
  type        = string
  description = "Pub/Sub topic name to trigger on"
}
