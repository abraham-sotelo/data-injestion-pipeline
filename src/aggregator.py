import boto3
import json
import sys
import time
import argparse
import os

# Name of your aggregation Lambda function
AGGREGATION_LAMBDA = "woven-data-pipeline-challenge-aggregation"

def invoke_aggregation_lambda():
  client = boto3.client("lambda")

  try:
    response = client.invoke(
      FunctionName=AGGREGATION_LAMBDA,
      InvocationType="RequestResponse"
    )
    payload = response["Payload"].read().decode("utf-8")
    result = json.loads(payload)

    print("--- 5 minutes aggregation ---")
    print(json.dumps(result, indent=2))

  except Exception as e:
    print(f"Error invoking Lambda: {e}")
    sys.exit(1)


def clear_screen():
    # Windows
    if os.name == "nt":
        os.system("cls")
    # Linux / Mac
    else:
        os.system("clear")


def parse_args():
  p = argparse.ArgumentParser(description="Invoke the aggregation Lambda function")
  p.add_argument("--interval", type=int, default=10, help="Seconds between invocations")
  p.add_argument("--once", action="store_true", help="Invoke only once")
  return p.parse_args()


if __name__ == "__main__":
  args = parse_args()
  if args.once:
    invoke_aggregation_lambda()
  else:
    try:
      while True:
        clear_screen()
        invoke_aggregation_lambda()
        time.sleep(args.interval)
    except KeyboardInterrupt:
      print("\nStopped aggregation loop.")