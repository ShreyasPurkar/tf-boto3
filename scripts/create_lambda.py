import boto3
import zipfile
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Resource configuration
aws_profile = os.environ.get("AWS_PROFILE")
region = os.environ.get("AWS_REGION")
bucket_name = os.environ.get("BUCKET_NAME")
lambda_name = "s3-upload-logger"
role_arn = os.environ.get("LAMBDA_ROLE_ARN")
account_id = os.environ.get("ACCOUNT_ID", "").strip('"')

# Start an AWS session using the profile configured
session = boto3.Session(profile_name=aws_profile)

# Create clients for Lambda and S3 services using the session
lambda_client = session.client("lambda", region_name=region)
s3_client = session.client("s3", region_name=region)
s3control = session.client("s3control", region_name=region)
s3_notification = session.client("s3", region_name=region)

# Create zip for Lambda
with zipfile.ZipFile("lambda.zip", "w") as z:
    z.write("lambda_function.py")

# Read the ZIP file content into memory
with open("lambda.zip", "rb") as f:
    zipped_code = f.read()

# Create the Lambda function
try:
    response = lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime="python3.11",
        Role=role_arn,
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": zipped_code},
        Timeout=15,
        Publish=True,
    )
    print("Lambda created:", response["FunctionArn"])
except lambda_client.exceptions.ResourceConflictException:
    print("Lambda already exists, skipping creation.")

# Allow S3 to invoke this Lambda on object upload
try:
    lambda_client.add_permission(
        FunctionName=lambda_name,
        StatementId="AllowS3Invoke",
        Action="lambda:InvokeFunction",
        Principal="s3.amazonaws.com",
        SourceArn=f"arn:aws:s3:::{bucket_name}",
    )
    print("Lambda permission added.")
    print("Waiting 5 seconds for permission to propagate...")
    time.sleep(5)
except lambda_client.exceptions.ResourceConflictException:
    print("Lambda permission already exists.")

# Configure S3 to invoke the Lambda function when a new object is uploaded
bucket_notification_config = {
    'LambdaFunctionConfigurations': [
        {
            'LambdaFunctionArn': (
                f"arn:aws:lambda:{region}:{account_id}:function:{lambda_name}"
            ),
            'Events': ['s3:ObjectCreated:*'],
        }
    ]
}

# Apply the notification configuration to the bucket
s3_notification.put_bucket_notification_configuration(
    Bucket=bucket_name,
    NotificationConfiguration=bucket_notification_config
)

print("S3 trigger added.")
