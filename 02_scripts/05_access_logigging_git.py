import boto3
import json
from botocore.exceptions import ClientError

REGION = 'ap-south-1'

s3 = boto3.client('s3', region_name=REGION)
account_id = 'your-aws-account-id'  # Replace with your actual 12-digit AWS Account ID

main_bucket = 'your-main-bucket-name'  # Replace with the name of the bucket to be logged
logging_bucket = 'your-logging-bucket-name'  # Replace with the bucket that will store the logs
logging_prefix = 'logs/'  # Folder path for logs in the logging bucket

def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" already exists.')
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print(f'Creating bucket "{bucket_name}" in region {REGION}...')
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': REGION}
            )
            print(f'Bucket "{bucket_name}" created.')
        else:
            print("Unexpected error:", e)

def set_logging_bucket_policy(bucket_name, main_bucket_name, account_id):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "S3ServerAccessLoggingPolicy",
                "Effect": "Allow",
                "Principal": {
                    "Service": "logging.s3.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
                "Condition": {
                    "ArnLike": {
                        "aws:SourceArn": f"arn:aws:s3:::{main_bucket_name}"
                    },
                    "StringEquals": {
                        "aws:SourceAccount": account_id
                    }
                }
            }
        ]
    }

    policy_json = json.dumps(policy)
    print(f'Setting bucket policy on "{bucket_name}"...')
    s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_json)
    print('Bucket policy set.')

def enable_access_logging(main_bucket_name, logging_bucket_name, logging_prefix):
    logging_config = {
        'LoggingEnabled': {
            'TargetBucket': logging_bucket_name,
            'TargetPrefix': logging_prefix
        }
    }
    print(f'Enabling access logging on "{main_bucket_name}"...')
    s3.put_bucket_logging(Bucket=main_bucket_name, BucketLoggingStatus=logging_config)
    print('Access logging enabled.')

def main():
    create_bucket(logging_bucket)
    set_logging_bucket_policy(logging_bucket, main_bucket, account_id)
    enable_access_logging(main_bucket, logging_bucket, logging_prefix)

if __name__ == "__main__":
    main()
