resource "cloudflare_r2_bucket" "dev-lake-weu" {
  account_id = var.cloudflare_account_id
  name       = "dev-lake-weu"
  location   = "weur"
}

# Note: R2 data catalog is not yet supported in the Cloudflare Terraform provider.

resource "cloudflare_r2_bucket_lifecycle" "dev-lake-weu-lifecycle" {
  account_id  = var.cloudflare_account_id
  bucket_name = cloudflare_r2_bucket.dev-lake-weu.id
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
