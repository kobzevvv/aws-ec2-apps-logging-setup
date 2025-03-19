aws iam create-role \
  --role-name Lambda-EC2-Logging-Manager \
  --assume-role-policy-document file://trust-policy-lambda.json
