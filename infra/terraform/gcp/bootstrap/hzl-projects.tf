module "project-hzl-apps" {
  source  = "terraform-google-modules/project-factory/google//modules/svpc_service_project"
  version = "~> 18.0"

  name            = "evedata-hzl-apps"
  project_id      = "evedata-hzl-apps"
  org_id          = var.org_id
  billing_account = var.billing_account
  folder_id       = local.folder_map["dqt"].id

  shared_vpc = module.vpc-hzl-shared.project_id
  shared_vpc_subnets = [
    try(module.vpc-hzl-shared.subnets["us-east1/subnet-hzl-ue1"].self_link, ""),
    try(module.vpc-hzl-shared.subnets["us-central1/subnet-hzl-uc1"].self_link, ""),
    try(module.vpc-hzl-shared.subnets["us-west1/subnet-hzl-uw1"].self_link, ""),
    try(module.vpc-hzl-shared.subnets["europe-north1/subnet-hzl-en1"].self_link, ""),
    try(module.vpc-hzl-shared.subnets["europe-north2/subnet-hzl-en2"].self_link, ""),
    try(module.vpc-hzl-shared.subnets["europe-west4/subnet-hzl-ew4"].self_link, ""),
  ]

  domain = data.google_organization.org.domain
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}

module "project-hzl-observability" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 18.0"

  name       = "evedata-hzl-observability"
  project_id = "evedata-hzl-observability"
  org_id     = var.org_id
  folder_id  = local.folder_map["hzl"].id

  billing_account = var.billing_account
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
  activate_apis = [
    "compute.googleapis.com",
    "monitoring.googleapis.com",
  ]
}

module "project-hzl-vpc-dqt" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 18.0"

  name       = "evedata-hzl-vpc-dqt"
  project_id = "evedata-hzl-vpc-dqt"
  org_id     = var.org_id
  folder_id  = local.folder_map["hzl"].id

  billing_account                = var.billing_account
  enable_shared_vpc_host_project = true
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}

module "project-hzl-vpc-hzl" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 18.0"

  name       = "evedata-hzl-vpc-hzl"
  project_id = "evedata-hzl-vpc-hzl"
  org_id     = var.org_id
  folder_id  = local.folder_map["hzl"].id

  billing_account                = var.billing_account
  enable_shared_vpc_host_project = true
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}

module "project-hzl-vpc-prd" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 18.0"

  name       = "evedata-hzl-vpc-prd"
  project_id = "evedata-hzl-vpc-prd"
  org_id     = var.org_id
  folder_id  = local.folder_map["hzl"].id

  billing_account                = var.billing_account
  enable_shared_vpc_host_project = true
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}
