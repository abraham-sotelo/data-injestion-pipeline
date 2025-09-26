#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
echo ">>> Running unit tests (unittest discovery)..."
python3 -m unittest discover tests -v -b
echo "All tests passed"