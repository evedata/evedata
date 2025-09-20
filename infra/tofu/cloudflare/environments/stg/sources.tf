resource "cloudflare_r2_bucket" "stg-sources-weu" {
  account_id = var.cloudflare_account_id
  name       = "stg-sources-weu"
  location   = "WEUR"
}
