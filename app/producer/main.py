#!python3
"""Streaming producer: read CSV and emit one JSON message per row at a cadence.

Simulates sensor-style streaming by reading csv file and writing one JSON object per row
Each emitted object includes two timestamp fields:
 - `ts_iso`: ISO-8601 UTC timestamp
 - `ts`: integer epoch seconds

Usage:
  python -m app.producer.main --rate-ms 100 --loop

Flags:
  --rate-ms N   : milliseconds between records (default 100)
  --limit N     : stop after N records (default: all rows). Use with --loop to stream continuously.
  --loop        : when reaching EOF, start again from the top (default: False)
"""
import csv
import json
import time
import boto3
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any


def row_to_json(row: Dict[str, Any]) -> str:
  """Return a JSON string for a single CSV row with timestamp enrichment.

  Adds:
    ts: ISO-8601 UTC timestamp
  """
  now = datetime.now(timezone.utc)
  enriched = dict(row)
  # Add timestamps in two formats to see what is more suitable for later processing
  enriched["ts"] = now.isoformat()
  return json.dumps(enriched, ensure_ascii=False)


def parse_args():
  p = argparse.ArgumentParser(description="Stream CSV rows as JSON at a cadence")
  p.add_argument("--rate-ms", type=int, default=100, help="Milliseconds between records (default 100)")
  p.add_argument("--limit", type=int, default=None, help="Maximum number of records to emit (default: all)")
  p.add_argument("--loop", action="store_true", help="Loop over the CSV indefinitely")
  p.add_argument("--csv-file", default=Path("Recommended_Fishing_Rivers_And_Streams.csv"), help="CSV file path")
  return p.parse_args()


def main():
  args = parse_args()
  repo_root = Path(__file__).resolve().parents[2]
  csv_file = repo_root / args.csv_file

  if not csv_file.exists():
    print(f"CSV file not found: {csv_file}")
    raise SystemExit(1)

  sqs = boto3.client("sqs", region_name="mx-central-1")
  queue_url = "https://sqs.mx-central-1.amazonaws.com/364218291784/woven-data-pipeline-challenge-sensor-data"

  emitted = 0
  try:
    while True:
      with csv_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
          response = sqs.send_message(QueueUrl=queue_url, MessageBody=row_to_json(row))
          print("Message sent. ID:", response["MessageId"])
          emitted += 1
          if args.limit is not None and emitted >= args.limit:
            print(f"Emitted {emitted} records", flush=True)
            return
          time.sleep(args.rate_ms / 1000.0)
      if not args.loop:
        break
    print(f"Emitted {emitted} records", flush=True)
    
  except KeyboardInterrupt:
    print(f"Interrupted. Emitted {emitted} records", flush=True)


if __name__ == "__main__":  # pragma: no cover
  main()
