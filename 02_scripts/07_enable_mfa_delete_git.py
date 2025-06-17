aws s3api put-bucket-versioning \
  --bucket your-bucket-name \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456"

(put this in terminal)

❗MFA Delete cannot be enabled or configured using Boto3 or AWS Console UI alone.

✅ It must be done using the AWS CLI and only when the bucket versioning is enabled.

✅ Steps to Enable MFA Delete (Manual via CLI)
Pre-requirements
Bucket must have versioning enabled.

You must be using root user credentials (not an IAM user).

You must have MFA already configured on the root account.

