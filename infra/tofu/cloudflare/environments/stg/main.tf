terraform {
  required_version = ">= 1.3"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.8.2"
    }
  }

  backend "gcs" {
    bucket = "evedata-terraform"
    prefix = "cloudflare/environments/stg"
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}
