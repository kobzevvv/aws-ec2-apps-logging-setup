# AWS CLI Configuration and Usage Guide

## Prerequisites
Before you start using AWS CLI, ensure you have the following:
- An AWS account
- AWS CLI installed on your system ([Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))
- IAM credentials (Access Key ID and Secret Access Key)

## Installing AWS CLI
### On Windows
Download and run the AWS CLI MSI installer from [AWS Downloads](https://aws.amazon.com/cli/).

### On macOS
```sh
brew install awscli
```

### On Linux
```sh
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

## Verifying Installation
```sh
aws --version
```
Expected output:
```
aws-cli/2.x.x Python/3.x.x ...
```

## Configuring AWS CLI
Run the following command to configure AWS CLI with your credentials:
```sh
aws configure
```
You'll be prompted to enter:
1. **AWS Access Key ID**
2. **AWS Secret Access Key**
3. **Default region name** (e.g., `us-east-1`)
4. **Default output format** (`json`, `text`, or `table`)

### Verify Configuration
```sh
aws sts get-caller-identity
```
This should return details about the IAM user or role.

## Common AWS CLI Commands

### List All S3 Buckets
```sh
aws s3 ls
```

### Upload a File to S3
```sh
aws s3 cp myfile.txt s3://my-bucket-name/
```

### List All EC2 Instances
```sh
aws ec2 describe-instances
```

### Start an EC2 Instance
```sh
aws ec2 start-instances --instance-ids i-xxxxxxxxxxxxxxxxx
```

### Stop an EC2 Instance
```sh
aws ec2 stop-instances --instance-ids i-xxxxxxxxxxxxxxxxx
```

### List IAM Users
```sh
aws iam list-users
```

### Check AWS CLI Configuration
```sh
aws configure list
```

## Using Named Profiles
If you work with multiple AWS accounts, use named profiles.
```sh
aws configure --profile my-profile
```
To use this profile:
```sh
aws s3 ls --profile my-profile
```

## Advanced Configuration
To edit AWS CLI configuration manually:
```sh
nano ~/.aws/config
```
Or for Windows:
```sh
notepad %USERPROFILE%\.aws\config
```

Example configuration:
```ini
[default]
region = us-east-1
output = json

[profile my-profile]
region = us-west-2
output = table
```

## Conclusion
AWS CLI is a powerful tool for managing AWS services. This guide covers the basics; refer to the [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/) for more details.
