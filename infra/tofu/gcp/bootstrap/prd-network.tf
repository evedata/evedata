module "vpc-prd-shared" {
  source  = "terraform-google-modules/network/google"
  version = "~> 9.0"

  project_id   = module.project-hzl-vpc-prd.project_id
  network_name = "vpc-prd-shared"

  subnets = [
    {
      subnet_name               = "subnet-prd-ue1"
      subnet_ip                 = "10.50.4.0/22"
      subnet_region             = "us-east1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-prd-uc1"
      subnet_ip                 = "10.50.36.0/22"
      subnet_region             = "us-central1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-prd-uw1"
      subnet_ip                 = "10.50.68.0/22"
      subnet_region             = "us-west1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-prd-en1"
      subnet_ip                 = "10.50.100.0/22"
      subnet_region             = "europe-north1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-prd-en2"
      subnet_ip                 = "10.50.132.0/22"
      subnet_region             = "europe-north2"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-prd-ew4"
      subnet_ip                 = "10.50.164.0/22"
      subnet_region             = "europe-west4"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
  ]

  firewall_rules = [
    {
      name      = "vpc-prd-shared-allow-icmp"
      direction = "INGRESS"
      priority  = 10000
      log_config = {
        metadata = "INCLUDE_ALL_METADATA"
      }
      allow = [
        {
          protocol = "icmp"
          ports    = []
        }
      ]
      ranges = [
        "10.50.0.0/16",
      ]
    },
    {
      name      = "vpc-prd-shared-allow-ssh"
      direction = "INGRESS"
      priority  = 10000
      log_config = {
        metadata = "INCLUDE_ALL_METADATA"
      }
      allow = [
        {
          protocol = "tcp"
          ports    = ["22"]
        }
      ]
      ranges = [
        "35.235.240.0/20",
      ]
    },
    {
      name      = "vpc-prd-shared-allow-rdp"
      direction = "INGRESS"
      priority  = 10000
      log_config = {
        metadata = "INCLUDE_ALL_METADATA"
      }
      allow = [
        {
          protocol = "tcp"
          ports    = ["3389"]
        }
      ]
      ranges = [
        "35.235.240.0/20",
      ]
    },
  ]
}
