import json
import boto3
import urllib.parse

# Create an S3 client using the default AWS credentials
s3 = boto3.client("s3")


# Lambda function to handle S3 events
# This function is triggered when a file is uploaded to the S3 bucket
def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Iterate through all records
    for record in event.get("Records", []):
        # Get the bucket name from the event
        bucket = record["s3"]["bucket"]["name"]
        # Get the object key and decode any URL-encoded characters
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        print(f"Uploaded file: {key} in bucket: {bucket}")

        # Set destination key for the copied object
        copy_key = f"copies/{key}"

        try:
            # Copy object to the new location in same bucket
            s3.copy_object(
                Bucket=bucket,
                CopySource={"Bucket": bucket, "Key": key},
                Key=copy_key
            )
            print(f"Copied {key} to {copy_key}")
        except Exception as e:
            print(f"Failed to copy object: {str(e)}")

    # Return a 200 OK response
    return {'statusCode': 200}
