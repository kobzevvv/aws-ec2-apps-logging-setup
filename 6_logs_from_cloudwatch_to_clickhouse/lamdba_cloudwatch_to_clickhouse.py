import boto3
import json
import requests
from datetime import datetime, timedelta

# AWS Config
LOG_GROUP = "/ec2-apps-usage"
REGION = "us-east-1"

# ClickHouse Config
CLICKHOUSE_URL = "http://your-clickhouse-server:8123"
CLICKHOUSE_DATABASE = "default"
CLICKHOUSE_TABLE = "cloudwatch_logs"

# Initialize AWS Clients
logs_client = boto3.client("logs", region_name=REGION)

def get_cloudwatch_logs():
    """Fetch logs from CloudWatch"""
    end_time = int(datetime.utcnow().timestamp() * 1000)  # Now
    start_time = int((datetime.utcnow() - timedelta(minutes=10)).timestamp() * 1000)  # Last 10 min

    response = logs_client.filter_log_events(
        logGroupName=LOG_GROUP,
        startTime=start_time,
        endTime=end_time,
        limit=100
    )

    logs = []
    for event in response.get("events", []):
        logs.append({
            "log_stream": event.get("logStreamName", ""),
            "timestamp": datetime.utcfromtimestamp(event["timestamp"] / 1000).isoformat(),
            "message": event["message"]
        })

    return logs

def insert_into_clickhouse(logs):
    """Insert logs into ClickHouse"""
    if not logs:
        print("No logs to insert")
        return

    insert_query = "INSERT INTO {}.{} (log_stream, timestamp, message) FORMAT JSONEachRow\n".format(
        CLICKHOUSE_DATABASE, CLICKHOUSE_TABLE
    )

    json_data = "\n".join(json.dumps(log) for log in logs)

    response = requests.post(
        CLICKHOUSE_URL, 
        data=insert_query + json_data
    )

    if response.status_code == 200:
        print("✅ Logs inserted successfully")
    else:
        print(f"❌ Error inserting logs: {response.text}")

def lambda_handler(event, context):
    logs = get_cloudwatch_logs()
    insert_into_clickhouse(logs)
    return {"status": "success", "logs_inserted": len(logs)}

