import os
import boto3
from datetime import datetime, timedelta, timezone
from collections import Counter

dynamodb = boto3.client("dynamodb")

RAW_TABLE = os.environ["RAW_TABLE"]
AGGREGATE_TABLE = os.environ["AGGREGATE_TABLE"]
PK_VALUE = "EVT"  # constant partition key

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(minutes=1)

    # Keys for BETWEEN (lexicographically sorted because ts starts with timestamp)
    start_key = one_minute_ago.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end_key = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    # Query the last 1 minute of events
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

    # Count per county
    county_counts = Counter()
    for item in items:
        county = item.get("county", {}).get("S")
        if county:
            county_counts[county] += 1

    # Store results in aggregate table
    for county, count in county_counts.items():
        dynamodb.put_item(
            TableName=AGGREGATE_TABLE,
            Item={
                "County": {"S": county},
                "count_last_1min": {"N": str(count)},
                "last_updated": {"S": now.isoformat()},
            },
        )

    print(f"Aggregated {len(items)} events across {len(county_counts)} counties")
    return {
        "statusCode": 200,
        "body": {
            "total_events": len(items),
            "county_counts": dict(county_counts),
        },
    }
