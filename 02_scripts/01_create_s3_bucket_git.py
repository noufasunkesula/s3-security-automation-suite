import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session(region_name="ap-south-1")
s3 = session.client("s3")

bucket_name = "your-bucket-name-here"  # Replace with your actual bucket name

try:
    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "ap-south-1"}
    )
    print("Bucket created:", response["Location"])
except ClientError as e:
    print("Error:", e.response["Error"]["Message"])
