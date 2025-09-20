resource "cloudflare_r2_bucket" "dev-sources-weu" {
  account_id = var.cloudflare_account_id
  name       = "dev-sources-weu"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket_lifecycle" "dev-sources-weu-lifecycle" {
  account_id  = var.cloudflare_account_id
  bucket_name = cloudflare_r2_bucket.dev-sources-weu.id
  rules = [
    {
      id = "Delete all objects and uploads after 7 days"
      conditions = {
        prefix = "/"
      }
      enabled = true
      delete_objects_transition = {
        condition = {
          max_age = 7
          type    = "Age"
        }
      }
      abort_multipart_uploads_transition = {
        condition = {
          max_age = 7
          type    = "Age"
        }
      }
    }
  ]
}
