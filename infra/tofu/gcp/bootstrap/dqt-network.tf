module "vpc-dqt-shared" {
  source  = "terraform-google-modules/network/google"
  version = "~> 9.0"

  project_id   = module.project-hzl-vpc-dqt.project_id
  network_name = "vpc-dqt-shared"

  subnets = [
    {
      subnet_name               = "subnet-dqt-ue1"
      subnet_ip                 = "10.50.8.0/22"
      subnet_region             = "us-east1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-dqt-uc1"
      subnet_ip                 = "10.50.40.0/22"
      subnet_region             = "us-central1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-dqt-uw1"
      subnet_ip                 = "10.50.72.0/22"
      subnet_region             = "us-west1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-dqt-en1"
      subnet_ip                 = "10.50.104.0/22"
      subnet_region             = "europe-north1"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-dqt-en2"
      subnet_ip                 = "10.50.136.0/22"
      subnet_region             = "europe-north2"
      subnet_private_access     = true
      subnet_flow_logs          = true
      subnet_flow_logs_sampling = "0.5"
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
    },
    {
      subnet_name               = "subnet-dqt-ew4"
      subnet_ip                 = "10.50.168.0/22"
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
      name      = "vpc-dqt-shared-allow-icmp"
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
      name      = "vpc-dqt-shared-allow-ssh"
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
      name      = "vpc-dqt-shared-allow-rdp"
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
