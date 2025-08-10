resource "google_monitoring_monitored_project" "monitored-projects" {
  for_each = toset([
    module.project-hzl-vpc-hzl.project_id,
    module.project-hzl-vpc-prd.project_id,
    module.project-hzl-vpc-dqt.project_id,
    module.project-hzl-apps.project_id,
    module.project-prd-apps.project_id,
    module.project-prd-data.project_id,
    module.project-dqt-apps.project_id,
    module.project-dqt-data.project_id,
  ])
  metrics_scope = "locations/global/metricsScopes/${module.project-hzl-observability.project_id}"
  name          = each.value
}
