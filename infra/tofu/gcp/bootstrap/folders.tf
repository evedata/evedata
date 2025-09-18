locals {
  folder_map = merge(
    { "hzl" = module.folder-hzl },
    { "dqt" = module.folder-dqt },
    { "prd" = module.folder-prd },
  )
}

module "folder-dqt" {
  source  = "terraform-google-modules/folders/google"
  version = "~> 5.0"

  parent = "organizations/${var.org_id}"
  names  = ["dqt"]
}

module "folder-hzl" {
  source  = "terraform-google-modules/folders/google"
  version = "~> 5.0"

  parent = "organizations/${var.org_id}"
  names  = ["hzl"]
}

module "folder-prd" {
  source  = "terraform-google-modules/folders/google"
  version = "~> 5.0"

  parent = "organizations/${var.org_id}"
  names  = ["prd"]
}

resource "time_sleep" "wait_for_folder_creations" {
  depends_on      = [module.folder-dqt, module.folder-hzl, module.folder-prd]
  create_duration = "60s"
}

resource "google_resource_manager_capability" "capability" {
  for_each = toset(var.application_enabled_folder_paths)

  provider        = google-beta
  value           = true
  parent          = local.folder_map[each.key].id
  capability_name = "app-management"
  depends_on      = [time_sleep.wait_for_folder_creations]
}
