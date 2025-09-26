#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

echo ">>> Building project before deployment"
source ./build.sh

cd infra
echo ">>> Deploying infrastructure with Terraform"
terraform init -input=false
terraform fmt -recursive
terraform plan
terraform apply -auto-approve