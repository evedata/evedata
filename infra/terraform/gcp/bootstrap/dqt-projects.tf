module "project-dqt-apps" {
  source  = "terraform-google-modules/project-factory/google//modules/svpc_service_project"
  version = "~> 18.0"

  name            = "evedata-dqt-apps"
  project_id      = "evedata-dqt-apps"
  org_id          = var.org_id
  billing_account = var.billing_account
  folder_id       = local.folder_map["dqt"].id

  shared_vpc = module.vpc-dqt-shared.project_id
  shared_vpc_subnets = [
    try(module.vpc-dqt-shared.subnets["us-east1/subnet-dqt-ue1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["us-central1/subnet-dqt-uc1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["us-west1/subnet-dqt-uw1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-north1/subnet-dqt-en1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-north2/subnet-dqt-en2"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-west4/subnet-dqt-ew4"].self_link, ""),
  ]

  domain     = data.google_organization.org.domain
  group_name = "gcp-organization-admins"
  group_role = "roles/editor"
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}

module "project-dqt-data" {
  source  = "terraform-google-modules/project-factory/google//modules/svpc_service_project"
  version = "~> 18.0"

  name            = "evedata-dqt-data"
  project_id      = "evedata-dqt-data"
  org_id          = var.org_id
  billing_account = var.billing_account
  folder_id       = local.folder_map["dqt"].id

  shared_vpc = module.project-hzl-vpc-dqt.project_id
  shared_vpc_subnets = [
    try(module.vpc-dqt-shared.subnets["us-east1/subnet-dqt-ue1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["us-central1/subnet-dqt-uc1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["us-west1/subnet-dqt-uw1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-north1/subnet-dqt-en1"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-north2/subnet-dqt-en2"].self_link, ""),
    try(module.vpc-dqt-shared.subnets["europe-west4/subnet-dqt-ew4"].self_link, ""),
  ]

  domain     = data.google_organization.org.domain
  group_name = "gcp-organization-admins"
  group_role = "roles/editor"
  depends_on = [
    module.org-policy-compute_skipDefaultNetworkCreation,
  ]
}
