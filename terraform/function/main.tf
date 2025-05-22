// terraform/function/main.tf

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../api/functions"
  output_path = "${path.module}/cv-parse-logger.zip"
}

resource "google_storage_bucket" "functions_bucket" {
  name     = "${var.project_id}-functions"
  location = var.region
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "cv-parse-logger.zip"
  bucket = google_storage_bucket.functions_bucket.name
  source = data.archive_file.function_zip.output_path
}

resource "google_cloudfunctions_function" "logger" {
  name        = "cv-parse-logger"
  project     = var.project_id
  region      = var.region
  runtime     = "python310"
  entry_point = "subscriber"

  source_archive_bucket = google_storage_bucket.functions_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = var.topic
  }

  available_memory_mb   = 128
  service_account_email = "${var.project_id}@appspot.gserviceaccount.com"
}
