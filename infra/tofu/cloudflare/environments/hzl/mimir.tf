resource "cloudflare_r2_bucket" "hzl-mimir-blocks-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-mimir-blocks-weu"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket" "hzl-mimir-alertmanager-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-mimir-alertmanager-weu"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket" "hzl-mimir-ruler-weu" {
  account_id = var.cloudflare_account_id
  name       = "hzl-mimir-ruler-weu"
  location   = "WEUR"
}
