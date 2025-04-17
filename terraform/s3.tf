# Generate UUID for bucket name to have unique bucket names globally unique across all AWS accounts.
resource "random_uuid" "bucket_name_uuid" {}

# Create S3 bucket with the generated UUID as the name
resource "aws_s3_bucket" "bucket" {
  bucket = random_uuid.bucket_name_uuid.result

  force_destroy = true

  tags = {
    Name = "csye6225-bucket"
  }
}

# Make the bucket ownership enforced
resource "aws_s3_bucket_ownership_controls" "bucket_owner_control" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Block the bucket from being publicly accessible
resource "aws_s3_bucket_public_access_block" "bucket_block_public_access" {
  bucket                  = aws_s3_bucket.bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Encrypt the bucket using server-side encryption with AES-256 encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# The bucket has a lifecycle rule to transition objects to the STANDARD_IA storage class after 30 days.
resource "aws_s3_bucket_lifecycle_configuration" "bucket_lifecycle_rule" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = var.s3_transition_days
      storage_class = var.s3_transition_storage_class
    }
  }
}

# Output the bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.id
}