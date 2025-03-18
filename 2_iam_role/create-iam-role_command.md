| Step | Command |
|------|---------|
| **Create Role** | ```aws iam create-role --role-name EC2-Logging-Role --assume-role-policy-document file://trust-policy.json``` |
| **Attach IAM Policies** | ```aws iam attach-role-policy --role-name EC2-Logging-Role --policy-arn <policy-arn>``` |
| **Create Instance Profile** | ```aws iam create-instance-profile --instance-profile-name EC2-Logging-Profile``` |
| **Add Role to Profile** | ```aws iam add-role-to-instance-profile --instance-profile-name EC2-Logging-Profile --role-name EC2-Logging-Role``` |
| **Attach to EC2** | ```aws ec2 associate-iam-instance-profile --instance-id i-xxxxxxxxxxxxxxxxx --iam-instance-profile Name=EC2-Logging-Profile``` |

