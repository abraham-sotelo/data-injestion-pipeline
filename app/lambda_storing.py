import boto3
import json
import os
from datetime import datetime

# AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment variables
BUCKET_NAME = "woven-data-pipeline-challenge-sensor-data-12345"
EVENTS_TABLE = "woven-data-pipeline-challenge-sensor-events"

table = dynamodb.Table(EVENTS_TABLE)


def lambda_handler(event, context):
    now = datetime.utcnow()

    for record in event["Records"]:
        body = json.loads(record["body"])

        # Write item to DynamoDB
        #expires_at = ts + 60  # Testing with one minute change later to 5
        item = {
            "pk": "EVT",
            #"sk": f"{ts}-{record['messageId']}",  # unique per message
            "ts": body["ts"],
            "county": body.get("County", "UNKNOWN"),
        }
        try:
            table.put_item(Item=item)
            print(f"Stored event {record['messageId']} in DynamoDB")
        except Exception as e:
            print(f"Failed to store in DynamoDB: {e}, body={body}")

    return {"statusCode": 200, "body": "Messages stored in S3 + DynamoDB"}
