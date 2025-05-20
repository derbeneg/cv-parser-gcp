// terraform/main.tf

module "gke" {
  source = "./gke"
  region = var.region
}

module "cloud_sql" {
  source = "./cloud_sql"
  region = var.region
}

module "pubsub" {
  source = "./pubsub"
  // no inputs needed here
}
