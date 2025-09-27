import os
import boto3
from datetime import datetime, timedelta, timezone
from collections import Counter
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    RAW_TABLE = os.environ["RAW_TABLE"]
    AGGREGATE_TABLE = os.environ["AGGREGATE_TABLE"]
    PK_VALUE = "EVT"  # constant partition key

    now = datetime.now(timezone.utc)
    window = now - timedelta(minutes=5)

    # Keys for BETWEEN (lexicographically sorted because ts starts with timestamp)
    start_key = window.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end_key = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    # Query the last 5 minutes of events
    items = []
    last_evaluated_key = None

    while True:
        params = {
            "TableName": RAW_TABLE,
            "KeyConditionExpression": "pk = :p AND ts BETWEEN :start AND :end",
            "ExpressionAttributeValues": {
                ":p": {"S": PK_VALUE},
                ":start": {"S": start_key},
                ":end": {"S": end_key},
            },
        }
        if last_evaluated_key:
            params["ExclusiveStartKey"] = last_evaluated_key

        response = dynamodb.query(**params)
        items.extend(response.get("Items", []))
        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    # Count per County
    County_counts = Counter()
    for item in items:
        County = item.get("County", {}).get("S")
        if County:
            County_counts[County] += 1

    # Store results in aggregate table
    item = {
        "updated": {"S": now.isoformat()},
        "total_events": {"N": str(len(items))},  # total events in the window
    }
    for County, count in County_counts.items():
        item[County] = {"N": str(count)}

    # Include test_run_id to avoid race condition in e2e tests
    if isinstance(event, dict) and "test_run_id" in event:
        item["test_run_id"] = {"S": event["test_run_id"]}

    dynamodb.put_item(
        TableName=AGGREGATE_TABLE,
        Item=item,
    )

    logger.info(f"Aggregated {len(items)} events across {len(County_counts)} counties")
    return {
        "statusCode": 200,
        "body": {
            "total_events": len(items),
            "County_counts": dict(County_counts),
        },
    }
