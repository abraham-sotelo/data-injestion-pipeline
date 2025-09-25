#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

VENV_DIR=".venv"
REQUIREMENTS_FILE="app/producer/requirements.txt"

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

echo ">>> Virtual environment setup complete!"
deactivate
