#!/bin/bash
set -euo pipefail

# Rate in ms: use first script argument if given, otherwise default to 100
RATE="${1:-100}"
# validate positive integer
if ! [[ "$RATE" =~ ^[0-9]+$ ]]; then
  echo "Warning: invalid rate '$RATE', defaulting to 100" >&2
  RATE=100
fi

cd "$(dirname "$0")"
echo ">>> Activating virtual environment"
source ".venv/bin/activate"
echo ">>> Running Data Streaming..."
python3 src/producer.py --rate-ms="$RATE" --loop