[![Terraform Validate](https://github.com/ShreyasPurkar/tf-boto3/actions/workflows/terraform-validations.yml/badge.svg)](https://github.com/ShreyasPurkar/tf-boto3/actions/workflows/terraform-validations.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
![Terraform](https://img.shields.io/badge/Terraform-v1.6+-623CE4?logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Deployed-orange?logo=amazon-aws)

# AWS Lambda S3 Trigger with Terraform & Boto3

This project sets up an AWS Lambda function that is automatically triggered whenever an object is uploaded to a specified S3 bucket. The Lambda function copies the uploaded object to a new location within the same bucket. Infrastructure is provisioned using Terraform, and Lambda deployment is handled via Python (Boto3).

---

## Features

- ✅ S3 bucket creation using Terraform
- ✅ Lambda function created using Boto3
- ✅ Lambda triggers on `s3:ObjectCreated:*` events
- ✅ Automatically copies uploaded files to a `copies/` folder in the same bucket
- ✅ All logs are sent to CloudWatch Logs
- ✅ Uses environment variables for flexibility

---

## Prerequisites

- AWS CLI installed and configured
- Python 3.8+
- Terraform
- An AWS account with sufficient IAM permissions

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone git@github.com:ShreyasPurkar/tf-boto3.git
cd tf-boto3-lambda
```

### 2. Provision Infrastructure with Terraform
```bash
terraform init
terraform apply 
```

### 3. Deploy the Lambda Function with Python
```bash
python create_lambda.py
```

### 4. You can upload a test file to the S3 bucket
```bash
python upload_test_file.py
```

### 5.  Verify Lambda Trigger
- Go to AWS Console → CloudWatch → Log Groups
- Open `/aws/lambda/s3-upload-logger`
- View the latest logs to see the original and copied object key

## References

### Terraform Documentation

### 1. S3 Bucket
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket#private-bucket-with-tags
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls#example-usage
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block#example-usage
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration#example-usage
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration#example-usage

### 2. IAM
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_access_key#example-usage
- https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_access_key#example-usage

### Boto3 Documentation

### 1. S3
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#s3

### 2. Lambda
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#lambda

