resource "cloudflare_dns_record" "evedata_io-cloudflare-mx-3" {
  content  = "route3.mx.cloudflare.net"
  name     = "evedata.io"
  priority = 49
  proxied  = false
  ttl      = 1
  type     = "MX"
  zone_id  = local.zone_map["evedata.io"].id
  settings = {}
}

resource "cloudflare_dns_record" "evedata_io-cloudflare-mx-2" {
  content  = "route2.mx.cloudflare.net"
  name     = "evedata.io"
  priority = 56
  proxied  = false
  ttl      = 1
  type     = "MX"
  zone_id  = local.zone_map["evedata.io"].id
  settings = {}
}

resource "cloudflare_dns_record" "evedata_io-cloudflare-mx-1" {
  content  = "route1.mx.cloudflare.net"
  name     = "evedata.io"
  priority = 37
  proxied  = false
  ttl      = 1
  type     = "MX"
  zone_id  = local.zone_map["evedata.io"].id
  settings = {}
}

resource "cloudflare_dns_record" "evedata_io-cloudflare-txt-dkim" {
  content  = "\"v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78k\" \"m4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB\""
  name     = "cf2024-1._domainkey.evedata.io"
  proxied  = false
  ttl      = 1
  type     = "TXT"
  zone_id  = local.zone_map["evedata.io"].id
  settings = {}
}

resource "cloudflare_dns_record" "evedata_io-cloudflare-txt-spf" {
  content  = "\"v=spf1 include:_spf.mx.cloudflare.net ~all\""
  name     = "evedata.io"
  proxied  = false
  ttl      = 1
  type     = "TXT"
  zone_id  = local.zone_map["evedata.io"].id
  settings = {}
}
