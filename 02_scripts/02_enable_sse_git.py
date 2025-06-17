import boto3
from botocore.exceptions import ClientError

bucket_name = "your-bucket-name-here"  # Replace with your actual bucket name

s3 = boto3.client("s3", region_name="ap-south-1")

try:
    s3.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
    )
    print(f"SSE-S3 encryption enabled on bucket: {bucket_name}")
except ClientError as e:
    print("Error:", e.response["Error"]["Message"])
