resource "cloudflare_r2_bucket" "stg-lake-weu" {
  account_id = var.cloudflare_account_id
  name       = "stg-lake-weu"
  location   = "weur"
}

# Note: R2 data catalog is not yet supported in the Cloudflare Terraform provider.
