import boto3
import os

BUCKET_NAME = 'your-bucket-name-here'  # Replace with your actual S3 bucket name
PREFIX = 'snow/'

# Replace these paths with your actual file locations
file_paths = [
    r'/path/to/snow0.jpg',  # root upload
    r'/path/to/snow/snow1.jpg',  # snow/ folder
    r'/path/to/snow/snow2.jpg'   # snow/ folder
]

s3 = boto3.client('s3')

for file_path in file_paths:
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        # Use prefix only for snow1.jpg and snow2.jpg
        if file_name in ['snow1.jpg', 'snow2.jpg']:
            s3_key = PREFIX + file_name
        else:
            s3_key = file_name  

        print(f'Uploading {file_name} to s3://{BUCKET_NAME}/{s3_key} ...')
        s3.upload_file(file_path, BUCKET_NAME, s3_key)
        print(f'Successfully uploaded: {s3_key}')
    else:
        print(f'Skipped: File not found - {file_path}')
