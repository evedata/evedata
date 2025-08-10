resource "cloudflare_dns_record" "evedata_io-txt-github-verification" {
  content  = "\"8410542d4e\""
  name     = "_gh-evedata-o"
  proxied  = false
  ttl      = 3600
  type     = "TXT"
  zone_id  = local.zone_map["evedata.dev"].id
  settings = {}
}
