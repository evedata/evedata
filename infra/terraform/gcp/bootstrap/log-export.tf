# random suffix to prevent collisions
resource "random_id" "suffix" {
  byte_length = 4
}

module "logsink-logbucketsink" {
  source  = "terraform-google-modules/log-export/google"
  version = "~> 11.0"

  destination_uri      = module.logging-destination.destination_uri
  log_sink_name        = "${var.org_id}-logbucketsink-${random_id.suffix.hex}"
  parent_resource_id   = var.org_id
  parent_resource_type = "organization"
  include_children     = true
  filter               = "logName: /logs/cloudaudit.googleapis.com%2Factivity OR logName: /logs/cloudaudit.googleapis.com%2Fsystem_event OR logName: /logs/cloudaudit.googleapis.com%2Fdata_access OR logName: /logs/cloudaudit.googleapis.com%2Faccess_transparency"
}

module "logging-destination" {
  source  = "terraform-google-modules/log-export/google//modules/logbucket"
  version = "~> 11.0"

  project_id               = module.project-hzl-observability.project_id
  name                     = "evedata-logging"
  location                 = "global"
  retention_days           = 30
  log_sink_writer_identity = module.logsink-logbucketsink.writer_identity
}
