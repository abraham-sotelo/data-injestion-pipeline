# Default variable values, edit this file or supply -var / -var-file

//aws_region = "ap-northeast-1"

lambda_runtime         = "python3.12"
storing_lambda_zip     = "../build/lambda_storing.zip"
aggregation_lambda_zip = "../build/lambda_aggregation.zip"

# SQS / Lambda tuning
sqs_lambda_batch_size = 1

# Schedule (disabled by default)
enable_aggregation_schedule     = true
aggregation_schedule_expression = "rate(1 minute)"
