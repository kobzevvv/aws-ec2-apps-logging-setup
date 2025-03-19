zip lambda-instance-log-setup-checker.zip lambda-instance-log-setup-checker.py
aws lambda create-function \
  --function-name InstanceLogSetupChecker \
  --runtime python3.9 \
  --role arn:aws:iam::<YOUR_ACCOUNT_ID>:role/Lambda-EC2-Logging-Manager \
  --handler lambda-instance-log-setup-checker.lambda_handler \
  --timeout 300 \
  --zip-file fileb://lambda-instance-log-setup-checker.zip
