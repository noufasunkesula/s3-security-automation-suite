import boto3
import json
from botocore.exceptions import ClientError

bucket_name = "your-bucket-name-here"  # Replace with your actual S3 bucket name
aws_account_id = "your-aws-account-id"  # Replace with your 12-digit AWS Account ID

s3 = boto3.client("s3", region_name="ap-south-1")

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowFullAccessToOwner",
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{aws_account_id}:root"},
            "Action": "s3:*",
            "Resource": [
                f"arn:aws:s3:::{bucket_name}",
                f"arn:aws:s3:::{bucket_name}/*"
            ]
        },
        {
            "Sid": "DenyPublicRead",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetBucketAcl",
                "s3:GetBucketPolicy"
            ],
            "Resource": [
                f"arn:aws:s3:::{bucket_name}",
                f"arn:aws:s3:::{bucket_name}/*"
            ],
            "Condition": {
                "Bool": {"aws:PrincipalIsAWSService": "false"},
                "StringNotEquals": {
                    "aws:PrincipalArn": f"arn:aws:iam::{aws_account_id}:root"
                }
            }
        }
    ]
}

try:
    bucket_policy_json = json.dumps(bucket_policy)
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
    print(f"Bucket policy applied successfully to {bucket_name}")
except ClientError as e:
    print("Error applying bucket policy:", e.response["Error"]["Message"])
