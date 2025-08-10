module "project-prd-apps" {
  source  = "terraform-google-modules/project-factory/google//modules/svpc_service_project"
  version = "~> 18.0"

  name            = "evedata-prd-apps"
  project_id      = "evedata-prd-apps"
  org_id          = var.org_id
  billing_account = var.billing_account
  folder_id       = local.folder_map["prd"].id

  shared_vpc = module.vpc-prd-shared.project_id
  shared_vpc_subnets = [
    try(module.vpc-prd-shared.subnets["us-east1/subnet-prd-ue1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["us-central1/subnet-prd-uc1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["us-west1/subnet-prd-uw1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-north1/subnet-prd-en1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-north2/subnet-prd-en2"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-west4/subnet-prd-ew4"].self_link, ""),
  ]

  domain = data.google_organization.org.domain
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}

module "project-prd-data" {
  source  = "terraform-google-modules/project-factory/google//modules/svpc_service_project"
  version = "~> 18.0"

  name            = "evedata-prd-data"
  project_id      = "evedata-prd-data"
  org_id          = var.org_id
  billing_account = var.billing_account
  folder_id       = local.folder_map["prd"].id

  shared_vpc = module.project-hzl-vpc-prd.project_id
  shared_vpc_subnets = [
    try(module.vpc-prd-shared.subnets["us-east1/subnet-prd-ue1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["us-central1/subnet-prd-uc1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["us-west1/subnet-prd-uw1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-north1/subnet-prd-en1"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-north2/subnet-prd-en2"].self_link, ""),
    try(module.vpc-prd-shared.subnets["europe-west4/subnet-prd-ew4"].self_link, ""),
  ]

  domain = data.google_organization.org.domain
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}
