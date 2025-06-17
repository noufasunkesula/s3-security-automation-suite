import boto3

s3 = boto3.client('s3')

bucket_name = 'your-bucket-name-here'  # Replace with your actual S3 bucket name

response = s3.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={
        'Status': 'Enabled'
    }
)

print(f"Versioning enabled on bucket: {bucket_name}")
