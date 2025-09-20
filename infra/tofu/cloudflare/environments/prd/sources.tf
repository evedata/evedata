resource "cloudflare_r2_bucket" "prd-sources-weu" {
  account_id = var.cloudflare_account_id
  name       = "prd-sources-weu"
  location   = "WEUR"
}
