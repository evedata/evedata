resource "cloudflare_r2_bucket" "hzl-loki-tsdb-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-loki-tsdb-weu"
  location   = "WEUR"
}
