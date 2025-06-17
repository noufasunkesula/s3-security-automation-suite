import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def is_public_statement(statement):
    return (
        "Principal" in statement and
        statement["Principal"] == "*" and
        statement.get("Effect") == "Allow"
    )

def check_and_remediate(bucket_name):
    print(f"\n🔍 Checking {bucket_name}...")

    try:
        # Get the bucket policy
        response = s3.get_bucket_policy(Bucket=bucket_name)
        policy = json.loads(response['Policy'])
        original_statements = policy.get("Statement", [])

        public_statements = [
            stmt for stmt in original_statements if is_public_statement(stmt)
        ]

        if public_statements:
            print(f"⚠️ PUBLIC POLICY FOUND in {bucket_name}")
            print("  - Public statements in policy:")
            for stmt in public_statements:
                print(json.dumps(stmt, indent=2))
        else:
            print(f"✅ {bucket_name} is private (no public policy).")
            return

        confirm = input("Do you want to remediate this? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Skipped policy remediation.")
            return

        updated_statements = [
            stmt for stmt in original_statements if not is_public_statement(stmt)
        ]

        if updated_statements:
            updated_policy = {
                "Version": policy.get("Version", "2012-10-17"),
                "Statement": updated_statements
            }
            s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(updated_policy))
            print(f"✅ Updated policy for {bucket_name}")
        else:
            s3.delete_bucket_policy(Bucket=bucket_name)
            print(f"✅ Deleted public-only policy from {bucket_name}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            print(f"✅ {bucket_name} has no bucket policy.")
        elif e.response['Error']['Code'] == 'AccessDenied':
            print(f"🚫 Access denied to check/update policy for {bucket_name}")
        else:
            print(f"[!] Error checking policy for {bucket_name}: {e}")

    # Check bucket ACL
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        grants = acl['Grants']
        public_grants = [
            g for g in grants if 'URI' in g['Grantee'] and (
                "AllUsers" in g['Grantee']['URI'] or
                "AuthenticatedUsers" in g['Grantee']['URI']
            )
        ]

        if public_grants:
            print(f"⚠️ Public ACL grants found in {bucket_name}")
            print(json.dumps(public_grants, indent=2))

            confirm_acl = input("Do you want to remove public ACL grants? (yes/no): ")
            if confirm_acl.lower() == "yes":
                s3.put_bucket_acl(Bucket=bucket_name, ACL='private')
                print(f"✅ ACL updated for {bucket_name}")
            else:
                print("❌ Skipped ACL remediation.")
        else:
            print(f"✅ No public ACL grants in {bucket_name}")

    except ClientError as e:
        print(f"[!] Error checking ACL for {bucket_name}: {e}")

def main():
    try:
        buckets = s3.list_buckets()
        for b in buckets['Buckets']:
            check_and_remediate(b['Name'])
    except ClientError as e:
        print(f"❌ Error listing buckets: {e}")

if __name__ == "__main__":
    main()
