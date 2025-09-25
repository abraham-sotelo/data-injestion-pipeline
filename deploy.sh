#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/infra"
echo ">>> Deploying infrastructure with Terraform"

zip -j lambda_storing.zip ../app/lambda_storing.py
zip -j lambda_aggregation.zip ../app/lambda_aggregation.py

terraform plan
terraform apply -auto-approve