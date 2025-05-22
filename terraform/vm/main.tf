// terraform/vm/main.tf

resource "google_compute_instance" "worker" {
  name         = "cv-parser-worker"
  project      = var.project_id
  zone         = var.zone
  machine_type = "e2-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network       = "default"
    access_config {}    # gives it a public IP
  }

  service_account {
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io google-cloud-sdk
    gcloud auth configure-docker --quiet
    docker run -d --restart unless-stopped -e PROJECT_ID=${var.project_id} -e PUBSUB_SUBSCRIPTION=cv-parse-sub gcr.io/${var.project_id}/cv-parser-worker:latest
  EOT

  tags = ["cv-parser-worker"]
}
