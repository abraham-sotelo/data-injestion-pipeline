# S3 bucket
#resource "aws_s3_bucket" "data_bucket" {
#  bucket = "${var.project_label}-sensor-data-12345"
#  tags   = {Project = var.project_label}
#}


# DynamoDB table to store raw events for last-5-minute window
locals {
  raw_events_table = "${var.project_label}-sensor-events"
  aggregates_table = "${var.project_label}-county_aggregates"
}

resource "aws_dynamodb_table" "sensor_events" {
  name         = local.raw_events_table
  billing_mode = "PAY_PER_REQUEST"

  # Primary key: constant pk + sortable sk (e.g. "ts#uuid")
  hash_key  = "pk"
  range_key = "ts"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "ts"
    type = "S"
  }

  # GSI: query per-county, ordered by time via sk
  attribute {
    name = "county"
    type = "S"
  }

  global_secondary_index {
    name            = "CountyIndex"
    hash_key        = "county"
    range_key       = "ts"
    projection_type = "ALL"
  }

  # TTL so items disappear ~5 minutes after arriva
  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  tags = {
    Project = var.project_label
  }
}

output "sensor_table_name" {
  value = aws_dynamodb_table.sensor_events.name
}


# 2. DynamoDB Aggregates table
resource "aws_dynamodb_table" "county_aggregates" {
  name         = local.aggregates_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "updated"

  attribute {
    name = "updated"
    type = "S"
  }

  tags = {
    Project = var.project_label
  }
}

output "aggregate_table_name" {
  value = aws_dynamodb_table.county_aggregates.name
}
