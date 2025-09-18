resource "cloudflare_r2_bucket" "hzl-tempo-traces-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-tempo-traces-weu"
  location   = "WEUR"
}
