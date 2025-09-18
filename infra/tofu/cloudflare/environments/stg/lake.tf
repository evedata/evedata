resource "cloudflare_r2_bucket" "stg-lake-weu" {
  account_id = var.cloudflare_account_id
  name       = "stg-lake-weu"
  location   = "WEUR"
}

resource "cloudflare_r2_bucket_lifecycle" "stg-lake-weu-lifecycle" {
  account_id  = var.cloudflare_account_id
  bucket_name = cloudflare_r2_bucket.stg-lake-weu.id
  rules = [
    {
      id = "Delete all objects and uploads after 90 days"
      conditions = {
        prefix = "/"
      }
      enabled = true
      delete_objects_transition = {
        condition = {
          max_age = 90
          type    = "Age"
        }
      }
      abort_multipart_uploads_transition = {
        condition = {
          max_age = 90
          type    = "Age"
        }
      }
    }
  ]
}
