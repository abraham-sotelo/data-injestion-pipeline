import os, unittest, subprocess, boto3, json
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from collections import Counter
from decimal import Decimal

RAW_TABLE = os.environ["RAW_TABLE"]
AGGREGATE_TABLE = os.environ["AGGREGATE_TABLE"]
AGGREGATION_LAMBDA_NAME = os.environ["AGGREGATION_LAMBDA_NAME"]

# Use DynamoDB resource API (cleaner marshalling to native Python types)
dynamodb = boto3.resource("dynamodb")
raw_table = dynamodb.Table(RAW_TABLE)
agg_table = dynamodb.Table(AGGREGATE_TABLE)

lambda_client = boto3.client("lambda")


def _normalize(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, Decimal):
            out[k] = int(v)  # or float(v) if you prefer
        else:
            out[k] = v
    return out


class TestPipelineE2E(unittest.TestCase):
    def test_pipeline_end_to_end(self):
        # Produce some new records
        print('\n')
        subprocess.run(["python3", "src/producer.py", "--limit", "50"], check=True)

        # Generate unique test ID
        test_run_id = str(uuid4())
        print(f">>> Using TEST_RUN_ID={test_run_id}")

        # Invoke aggregation Lambda with test ID
        lambda_client.invoke(
            FunctionName=AGGREGATION_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps({"test_run_id": test_run_id})
        )

        # 4. Scan aggregates table for test ID
        agg_resp = agg_table.scan(
            FilterExpression="test_run_id = :id",
            ExpressionAttributeValues={":id": test_run_id}
        )
        self.assertEqual(len(agg_resp["Items"]), 1, "No aggregate row found for this test run")
        latest = agg_resp["Items"][0]

        # Determine the 5-minute window used by the aggregation Lambda
        updated_dt = datetime.fromisoformat(latest["updated"].replace("Z", "+00:00"))
        window_start = updated_dt - timedelta(minutes=5)

        # Query sensor table for the same window used by the aggregation Lambda
        start_key = window_start.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        end_key = updated_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")

        items = []
        lek = None
        while True:
            params = {
                "KeyConditionExpression": "pk = :p AND ts BETWEEN :start AND :end",
                "ExpressionAttributeValues": {
                    ":p": "EVT",
                    ":start": start_key,
                    ":end": end_key,
                },
                "ConsistentRead": True,
            }
            if lek:
                params["ExclusiveStartKey"] = lek
            resp = raw_table.query(**params)
            items.extend(resp["Items"])
            lek = resp.get("LastEvaluatedKey")
            if not lek:
                break

        # Calculate aggregation from sensor table items
        local_counts = Counter()
        for it in items:
            County = it.get("County")
            if County:
                local_counts[County] += 1
        local_total = len(items)

        # Aggregation values from aggregates table
        agg_total = latest["total_events"]
        agg_counts = {
            k: v for k, v in latest.items()
            if k not in ("updated", "total_events", "test_run_id")
        }
        agg_counts = _normalize(agg_counts)

        # Debug output
        print("\n--- Local Aggregation ---")
        print(f"Total events: {local_total}")
        print(dict(local_counts))

        print("\n--- DynamoDB Aggregation ---")
        print(f"Total events: {agg_total}")
        print(agg_counts)

        # Assertions
        self.assertEqual(agg_total, local_total, f"Total mismatch. agg={agg_total}, local={local_total}")
        self.assertEqual(agg_counts, dict(local_counts), f"Per-County mismatch.\nagg={agg_counts}\nlocal={dict(local_counts)}")


if __name__ == "__main__":
    unittest.main()
