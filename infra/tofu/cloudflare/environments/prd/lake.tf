resource "cloudflare_r2_bucket" "prd-lake-weu" {
  account_id = var.cloudflare_account_id
  name       = "prd-lake-weu"
  location   = "WEUR"
}

# Note: R2 data catalog is not yet supported in the Cloudflare Terraform provider.
