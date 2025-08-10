variable "billing_account" {
  description = "The ID of the billing account to associate projects with"
  type        = string
}

variable "org_id" {
  description = "The organization id for the associated resources"
  type        = string
}

variable "billing_project" {
  description = "The project id to use for billing"
  type        = string
}

variable "application_enabled_folder_paths" {
  description = "The folder paths to enable resource manager capability"
  type        = list(any)
  default = [
    "hzl",
    "dqt",
    "prd",
  ]
}
