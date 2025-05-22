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

module "vm" {
  source     = "./vm"
  project_id = var.project_id
  region     = var.region
  zone       = var.zone
}

module "function" {
  source     = "./function"
  project_id = var.project_id
  region     = var.region
  topic      = module.pubsub.topic_name
}