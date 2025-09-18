module "gg-gcp-hzl-admins" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-hzl-admins@evedata.io"
  display_name = "gcp-hzl-admins"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-hzl-admins" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["hzl"].id,
  ]
  bindings = {
    "roles/editor" = [
      "group:${module.gg-gcp-hzl-developers.id}",
    ],
  }
}

module "gg-gcp-hzl-developers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-hzl-developers@evedata.io"
  display_name = "gcp-hzl-developers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-hzl-developers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["hzl"].id,
  ]
  bindings = {
    "roles/compute.instanceAdmin.v1" = [
      "group:${module.gg-gcp-hzl-developers.id}",
    ],
    "roles/container.admin" = [
      "group:${module.gg-gcp-hzl-developers.id}",
    ],
  }
}

module "gg-gcp-hzl-viewers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-hzl-viewers@evedata.io"
  display_name = "gcp-hzl-viewers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-hzl-viewers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["hzl"].id,
  ]
  bindings = {
    "roles/viewer" = [
      "group:${module.gg-gcp-hzl-viewers.id}",
    ],
  }
}

module "projects-iam-hzl-observability-gcp-logging-monitoring-viewers" {
  source  = "terraform-google-modules/iam/google//modules/projects_iam"
  version = "~> 8.0"

  projects = [
    module.project-hzl-observability.project_id,
  ]
  bindings = {
    "roles/bigquery.dataViewer" = [
      "group:gcp-logging-monitoring-viewers@evedata.io",
    ],
    "roles/monitoring.viewer" = [
      "group:gcp-logging-monitoring-viewers@evedata.io",
    ]
    "roles/logging.viewer" = [
      "group:gcp-logging-monitoring-viewers@evedata.io",
    ],
    "roles/logging.privateLogViewer" = [
      "group:gcp-logging-monitoring-viewers@evedata.io",
    ],
    "roles/pubsub.viewer" = [
      "group:gcp-logging-monitoring-viewers@evedata.io",
    ],
  }
}

module "projects-iam-hzl-observability-gcp-security-admins" {
  source  = "terraform-google-modules/iam/google//modules/projects_iam"
  version = "~> 8.0"

  projects = [
    module.project-hzl-observability.project_id,
  ]
  bindings = {
    "roles/bigquery.dataViewer" = [
      "group:gcp-security-admins@evedata.io",
    ],
    "roles/pubsub.viewer" = [
      "group:gcp-security-admins@evedata.io",
    ],
  }
}
