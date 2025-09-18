resource "cloudflare_r2_bucket" "hzl-pyroscope-blocks-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-pyroscope-blocks-weu"
  location   = "weur"
}
