# 1. Create the S3 Bucket
resource "aws_s3_bucket" "unsecure_bucket" {
  bucket = "lab03-scan-bucket"
}

# 2. Allow all public access 
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket                  = aws_s3_bucket.unsecure_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

