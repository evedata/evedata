module "gg-gcp-dqt-admins" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-dqt-admins@evedata.io"
  display_name = "gcp-dqt-admins"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-dqt-admins" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["dqt"].id,
  ]
  bindings = {
    "roles/editor" = [
      "group:${module.gg-gcp-dqt-developers.id}",
    ],
  }
}

module "gg-gcp-dqt-developers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-dqt-developers@evedata.io"
  display_name = "gcp-dqt-developers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-dqt-developers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["dqt"].id,
  ]
  bindings = {
    "roles/compute.instanceAdmin.v1" = [
      "group:${module.gg-gcp-dqt-developers.id}",
    ],
    "roles/container.admin" = [
      "group:${module.gg-gcp-dqt-developers.id}",
    ],
  }
}

module "gg-gcp-dqt-viewers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-dqt-viewers@evedata.io"
  display_name = "gcp-dqt-viewers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-dqt-viewers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["dqt"].id,
  ]
  bindings = {
    "roles/viewer" = [
      "group:${module.gg-gcp-dqt-viewers.id}",
    ],
  }
}
