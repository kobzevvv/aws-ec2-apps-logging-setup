#!/bin/bash

# Load environment variables from .env file (if exists)
if [ -f "/etc/ec2-logging.env" ]; then
    source /etc/ec2-logging.env
fi

# Default values if variables are not set in .env
USE_CLOUDWATCH=${USE_CLOUDWATCH:-true}
S3_BUCKET=${S3_BUCKET:-"s3://default-bucket"}

# Variables
LOG_FILE="/var/log/ec2-apps-usage.log"
CLOUDWATCH_CONFIG="/opt/aws/amazon-cloudwatch-agent/bin/config.json"

# Install CloudWatch Agent if not installed
if ! command -v amazon-cloudwatch-agent &> /dev/null; then
    echo "Installing CloudWatch Agent..."
    sudo yum install -y amazon-cloudwatch-agent || sudo apt-get install -y amazon-cloudwatch-agent
fi

# Create CloudWatch Agent Config
echo "Setting up CloudWatch Agent configuration..."
sudo tee $CLOUDWATCH_CONFIG > /dev/null <<EOL
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "$LOG_FILE",
            "log_group_name": "/ec2-apps-usage",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOL

# Start CloudWatch Agent if enabled
if [ "$USE_CLOUDWATCH" = true ]; then
    echo "Starting CloudWatch Agent..."
    sudo amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:$CLOUDWATCH_CONFIG -s
fi

# Create script for collecting logs
echo "Creating application logging script..."
sudo tee /usr/local/bin/collect-app-logs.sh > /dev/null <<'EOL'
#!/bin/bash
LOG_FILE="/var/log/ec2-apps-usage.log"

echo "=== Logging Applications at $(date) ===" >> $LOG_FILE
ps aux --sort=-%mem | head -20 >> $LOG_FILE
echo "" >> $LOG_FILE

if [ "$USE_CLOUDWATCH" = false ]; then
    aws s3 cp $LOG_FILE $S3_BUCKET/$(hostname)-$(date +%Y-%m-%d_%H-%M-%S).log
fi
EOL

# Make script executable
sudo chmod +x /usr/local/bin/collect-app-logs.sh

# Set up cron job to run the script every 5 minutes
echo "Setting up cron job..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/collect-app-logs.sh") | crontab -

echo "✅ EC2 Applications Logging Setup Complete!"
