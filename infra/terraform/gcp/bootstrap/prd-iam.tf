module "gg-gcp-prd-admins" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-prd-admins@evedata.io"
  display_name = "gcp-prd-admins"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-prd-admins" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["prd"].id,
  ]
  bindings = {
    "roles/editor" = [
      "group:${module.gg-gcp-prd-developers.id}",
    ],
  }
}

module "gg-gcp-prd-developers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-prd-developers@evedata.io"
  display_name = "gcp-prd-developers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-prd-developers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["prd"].id,
  ]
  bindings = {
    "roles/compute.instanceAdmin.v1" = [
      "group:${module.gg-gcp-prd-developers.id}",
    ],
    "roles/container.admin" = [
      "group:${module.gg-gcp-prd-developers.id}",
    ],
  }
}

module "gg-gcp-prd-viewers" {
  source  = "terraform-google-modules/group/google"
  version = "~> 0.6"

  id           = "gcp-prd-viewers@evedata.io"
  display_name = "gcp-prd-viewers"
  customer_id  = data.google_organization.org.directory_customer_id
  types = [
    "default",
    "security",
  ]
}

module "folders-iam-prd-viewers" {
  source  = "terraform-google-modules/iam/google//modules/folders_iam"
  version = "~> 8.0"

  folders = [
    local.folder_map["prd"].id,
  ]
  bindings = {
    "roles/viewer" = [
      "group:${module.gg-gcp-prd-viewers.id}",
    ],
  }
}
