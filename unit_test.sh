#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
source ".venv/bin/activate"
echo ">>> Running unit tests (unittest discovery)..."
export QUEUE_URL=queue_url
export RAW_TABLE=event_table

echo ">>> Running unit tests (unittest discovery)..."
python3 -m unittest discover tests -v -b
echo "All tests passed"