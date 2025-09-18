locals {
  zone_map = merge(
    { "evedata.dev" = cloudflare_zone.evedata_dot_dev },
  )
}

resource "cloudflare_zone" "evedata_dot_dev" {
  name    = "evedata.dev"
  account = { id = var.cloudflare_account_id }
  type    = "full"
}
