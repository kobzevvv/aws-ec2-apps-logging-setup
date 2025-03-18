### Overview
This repository provides code templates and a step-by-step guide to automatically set up monitoring and logging of application usage on EC2 instances. The setup ensures that logs about running applications are collected, stored, and optionally sent to external logging services like CloudWatch, S3, or Telegram.

### Features
- Automated setup – No manual configuration needed for new instances.
- Tracks active applications – Logs currently running applications with CPU/memory usage.
- Works across multiple EC2 instances – Applies monitoring automatically.
- Supports various log destinations – AWS CloudWatch, S3, Telegram, or custom log collectors.
- Uses IAM roles & AWS Systems Manager (SSM) – Secure and scalable solution.

### Step-by-Step: Setting Up EC2 Applications Logging
- Set Up AWS CLI
- Create IAM Role for EC2 Logging
- Update Environment to Use the Role
- Set Monitoring & Log Destination
- Deploy CloudFormation for Auto Setup
- Run Tests: Ensure All Instances Send Logs