#!/bin/bash
set -euo pipefail

SECONDS="${1:-10}"
# validate positive integer
if ! [[ "$SECONDS" =~ ^[0-9]+$ ]]; then
  echo "Warning: invalid seconds '$SECONDS', defaulting to 10" >&2
  SECONDS=10
fi

cd "$(dirname "$0")"
echo ">>> Activating virtual environment"
source ".venv/bin/activate"
echo ">>> Running Data Streaming..."
python3 src/aggregator.py --interval="$SECONDS"