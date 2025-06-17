import boto3

BUCKET_NAME = 'your-bucket-name'  # Replace with your S3 bucket name
PREFIX = 'your-folder-prefix/'    # e.g., 'images/', 'logs/', etc.

s3 = boto3.client('s3')

def list_objects_with_prefix(bucket, prefix):
    print(f"Listing objects in bucket '{bucket}' with prefix '{prefix}':\n")
    
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print(f"No objects found with prefix '{prefix}'.")

# Run the function
list_objects_with_prefix(BUCKET_NAME, PREFIX)
