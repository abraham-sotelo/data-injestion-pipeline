#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

echo ">>> Creating virtual environment in $VENV_DIR"
python3 -m venv "$VENV_DIR"
echo ">>> Activating virtual environment"
source "$VENV_DIR/bin/activate"
echo ">>> Upgrading pip"
pip install --upgrade pip

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo ">>> Installing dependencies from $REQUIREMENTS_FILE"
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "$REQUIREMENTS_FILE not found. Skipping dependency installation."
fi
deactivate
echo ">>> Virtual environment setup complete!"

echo ">>> Checking Python syntax"
python3 -m py_compile src/*.py

echo ">>> Running unit tests"
./unit_test.sh

echo ">>> Packaging Lambda functions"
mkdir -p build
rm -f build/lambda_storing.zip build/lambda_aggregation.zip
zip -j build/lambda_storing.zip src/lambda_storing.py
zip -j build/lambda_aggregation.zip src/lambda_aggregation.py