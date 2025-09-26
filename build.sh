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

CSV_FILE="Recommended_Fishing_Rivers_And_Streams.csv"
CSV_URL="https://data.ny.gov/api/views/jcxg-7gnm/rows.csv?accessType=DOWNLOAD"

echo ">>> Checking for $CSV_FILE"
if [ -f "$CSV_FILE" ]; then
    echo ">>> $CSV_FILE already exists. Skipping download."
else
    echo ">>> $CSV_FILE not found. Downloading from $CSV_URL"
    curl -fSL -o "$CSV_FILE" "$CSV_URL"
    echo ">>> Download complete: $CSV_FILE"
fi