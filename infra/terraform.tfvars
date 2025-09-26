# Default variable values (developers can edit this file or supply -var / -var-file)
aws_region = "mx-central-1"

# Optional overrides (commented examples)
# sensor_queue_name = "custom-sensor-queue"
# raw_events_table_name = "custom-raw-events"
# aggregates_table_name = "custom-aggregates"

lambda_runtime         = "python3.12"
storing_lambda_zip     = "../build/lambda_storing.zip"
aggregation_lambda_zip = "../build/lambda_aggregation.zip"

# SQS / Lambda tuning
sqs_lambda_batch_size = 1

# Schedule (disabled by default)
enable_aggregation_schedule     = false
aggregation_schedule_expression = "rate(1 minute)"
