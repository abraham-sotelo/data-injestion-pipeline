variable "project_label" {
  description = "Base label for resources"
  default     = "woven-data-pipeline-challenge-asotelo"
}

variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "mx-central-1"
}

# SQS Queue configuration
variable "sensor_queue_name" {
  description = "Explicit SQS queue name (leave null to auto-compose from project_label)"
  type        = string
  default     = null
}

variable "sensor_queue_visibility_timeout" {
  description = "Visibility timeout in seconds"
  type        = number
  default     = 30
}

variable "sensor_queue_retention_seconds" {
  description = "Message retention period in seconds"
  type        = number
  default     = 3600
}

variable "sensor_queue_delay_seconds" {
  description = "Delivery delay for new messages"
  type        = number
  default     = 0
}

variable "sensor_queue_max_message_size" {
  description = "Max message size (bytes)"
  type        = number
  default     = 1024
}

variable "sensor_queue_receive_wait_seconds" {
  description = "Long polling wait time (seconds)"
  type        = number
  default     = 1
}

variable "sqs_lambda_batch_size" {
  description = "Batch size for SQS -> Lambda event source mapping"
  type        = number
  default     = 1
}


# DynamoDB table configuration
variable "raw_events_table_name" {
  description = "Override for raw sensor events table name"
  type        = string
  default     = null
}

variable "aggregates_table_name" {
  description = "Override for county aggregates table name"
  type        = string
  default     = null
}

# Lambda configuration
variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.12"
}

variable "storing_lambda_zip" {
  description = "Path to storing lambda deployment package"
  type        = string
  default     = "../build/lambda_storing.zip"
}

variable "aggregation_lambda_zip" {
  description = "Path to aggregation lambda deployment package"
  type        = string
  default     = "../build/lambda_aggregation.zip"
}

# Scheduler / EventBridge
variable "enable_aggregation_schedule" {
  description = "Whether to enable the EventBridge schedule for the aggregation lambda"
  type        = bool
  default     = false
}

variable "aggregation_schedule_expression" {
  description = "Schedule expression for EventBridge rule"
  type        = string
  default     = "rate(1 minute)"
}
