locals {
  zone_map = merge(
    { "evedata.guide" = cloudflare_zone.evedata_dot_guide },
    { "evedata.io" = cloudflare_zone.evedata_dot_io }
  )
}

resource "cloudflare_zone" "evedata_dot_guide" {
  name    = "evedata.guide"
  type    = "full"
  account = { id = var.cloudflare_account_id }
}

resource "cloudflare_zone" "evedata_dot_io" {
  name    = "evedata.io"
  account = { id = var.cloudflare_account_id }
  type    = "full"
}
