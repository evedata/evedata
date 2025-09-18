terraform {
  required_version = ">= 1.3"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.34"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 6.34"
    }
    random = {
      source = "hashicorp/random"
      version = ">= 3.7"
    }
    time = {
      source = "hashicorp/time"
      version = ">= 0.13"
    }
  }

  backend "gcs" {
    bucket = "evedata-terraform"
    prefix = "gcp/bootstrap"
  }
}

# Required if using User ADCs (Application Default Credentials) for Org Policy API.
provider "google" {
  user_project_override = true
  billing_project       = var.billing_project
  default_labels = {
    goog-cloudsetup = "downloaded"
  }
}

# Required if using User ADCs (Application Default Credentials) for Cloud Identity API.
provider "google-beta" {
  user_project_override = true
  billing_project       = var.billing_project
}
