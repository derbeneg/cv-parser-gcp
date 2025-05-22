// terraform/vm/variables.tf

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region for the VM"
}

variable "zone" {
  type        = string
  description = "GCP zone for the VM"
  default     = "us-central1-a"
}
