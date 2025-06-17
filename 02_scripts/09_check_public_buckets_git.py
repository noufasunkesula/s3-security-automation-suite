import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def is_block_public_access_disabled(bucket_name):
    try:
        response = s3.get_bucket_policy_status(Bucket=bucket_name)
        return response['PolicyStatus']['IsPublic']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return False
        else:
            print(f"[!] Error checking policy status for {bucket_name}: {e}")
            return False

def is_acl_public(bucket_name):
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        for grant in acl['Grants']:
            grantee_uri = grant['Grantee'].get('URI', '')
            if 'AllUsers' in grantee_uri or 'AuthenticatedUsers' in grantee_uri:
                return True
        return False
    except ClientError as e:
        print(f"[!] Error checking ACL for {bucket_name}: {e}")
        return False

def main():
    buckets = s3.list_buckets()
    print("🔍 Checking public access on all S3 buckets...\n")

    for bucket in buckets['Buckets']:
        name = bucket['Name']
        is_public_policy = is_block_public_access_disabled(name)
        is_public_acl = is_acl_public(name)

        if is_public_policy or is_public_acl:
            print(f"⚠️ PUBLIC BUCKET FOUND: {name}")
            if is_public_policy:
                print("  - Bucket policy allows public access")
            if is_public_acl:
                print("  - ACL allows public access\n")
        else:
            print(f"✅ {name} is private.")

if __name__ == "__main__":
    main()
