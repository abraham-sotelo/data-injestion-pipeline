#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
source ".venv/bin/activate"

echo ">>> Running end-to-end tests"
export QUEUE_URL=$(terraform -chdir=infra output -raw sensor_queue_url)
export RAW_TABLE=$(terraform -chdir=infra output -raw sensor_table_name)
export AGGREGATE_TABLE=$(terraform -chdir=infra output -raw aggregate_table_name)
export AGGREGATION_LAMBDA_NAME=$(terraform -chdir=infra output -raw aggregation_lambda_name)
python3 -m unittest discover -s tests/e2e -p "test_*.py" -v