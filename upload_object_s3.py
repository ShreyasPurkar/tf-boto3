import boto3
import os

# Resource configuration
aws_profile = os.environ.get("AWS_PROFILE")
bucket_name = os.environ.get("BUCKET_NAME")
file_path = "test.txt"

# Load AWS session using configured profile
session = boto3.Session(profile_name=aws_profile)
s3 = session.client("s3")

# Create a test file
with open(file_path, "w") as f:
    f.write("This is a test file to be uploaded on S3.")

# Upload to S3
s3.upload_file(file_path, bucket_name, file_path)

print(f"Uploaded {file_path} to {bucket_name}")
