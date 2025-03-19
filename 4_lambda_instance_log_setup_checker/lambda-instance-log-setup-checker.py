import boto3
import os

# AWS Clients
ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")

# S3 Bucket URL or GitHub raw link where the setup script is stored
SETUP_SCRIPT_URL = "https://my-bucket.s3.amazonaws.com/setup-ec2-logging.sh"

# Name of the IAM Role that instances should have
IAM_ROLE_NAME = "EC2-Logging-Profile"

def get_instances_without_logging():
    """Finds EC2 instances that do not have logging enabled."""
    instances_to_fix = []
    
    # Get all running instances
    response = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
    
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            iam_instance_profile = instance.get("IamInstanceProfile", {}).get("Arn", "")

            # Check if instance has the correct IAM role
            if IAM_ROLE_NAME not in iam_instance_profile:
                print(f"❌ {instance_id} is missing the IAM role")
                instances_to_fix.append(instance_id)
                continue  # Skip checking logs if role is missing

            # Check if instance has logs by searching for running CloudWatch Agent
            try:
                response = ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={"commands": ["pgrep amazon-cloudwatch-agent || echo 'MISSING'"]},
                    TimeoutSeconds=10
                )
                command_id = response["Command"]["CommandId"]
                
                # Wait for command result
                result = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
                if "MISSING" in result["StandardOutputContent"]:
                    print(f"❌ {instance_id} does NOT have CloudWatch Agent running")
                    instances_to_fix.append(instance_id)
            except Exception as e:
                print(f"⚠️ Error checking instance {instance_id}: {e}")

    return instances_to_fix

def install_logging(instance_id):
    """Triggers the log setup script on the given instance using AWS SSM."""
    print(f"🚀 Installing logging on {instance_id}...")
    
    try:
        ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [f"curl -s {SETUP_SCRIPT_URL} | bash"]},
            TimeoutSeconds=600
        )
        print(f"✅ Logging setup triggered on {instance_id}")
    except Exception as e:
        print(f"❌ Failed to install logging on {instance_id}: {e}")

def lambda_handler(event, context):
    """Main Lambda function to check and fix instances without logging."""
    print("🔍 Checking EC2 instances for missing logging...")
    
    instances_to_fix = get_instances_without_logging()
    if not instances_to_fix:
        print("✅ All instances have logging enabled!")
        return {"status": "success", "message": "No missing logs detected"}

    for instance_id in instances_to_fix:
        install_logging(instance_id)

    return {"status": "success", "message": f"Fixed {len(instances_to_fix)} instances"}
