resource "google_sql_database_instance" "postgres" {
  name             = "cv-parser-db"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "app_db" {
  name     = "app"
  instance = google_sql_database_instance.postgres.name
}