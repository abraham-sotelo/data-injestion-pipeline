import boto3
import json
import os
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment variables
RAW_TABLE = os.environ["RAW_TABLE"]

table = dynamodb.Table(RAW_TABLE)


def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        ts_dt = datetime.fromisoformat(body["ts"])

        # Write item to DynamoDB
        item = {
            "pk": "EVT",
            "ts": body["ts"],
            "county": body.get("County", "UNKNOWN"),
            "expires_at": int((ts_dt + timedelta(minutes=6)).timestamp())
        }
        try:
            table.put_item(Item=item)
            logger.info(f"Stored event {record['messageId']} in DynamoDB")
        except Exception as e:
            logger.error(f"Failed to store in DynamoDB: {e}, body={body}")

    return {"statusCode": 200, "body": "Messages stored in S3 + DynamoDB"}
