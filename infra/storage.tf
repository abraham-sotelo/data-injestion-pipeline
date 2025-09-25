# S3 bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_label}-sensor-data-12345"
  tags   = {Project = var.project_label}
}


# DynamoDB table to store raw events for last-5-minute window
resource "aws_dynamodb_table" "sensor_events" {
  name         = "${var.project_label}-sensor-events"
  billing_mode = "PAY_PER_REQUEST"

  # Primary key lets us efficiently query by time window
  hash_key  = "pk"  # constant partition key
  range_key = "sk"  # sort key

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  # Optional: GSI to query per-county, ordered by time
  attribute {
    name = "county"
    type = "S"
  }

  global_secondary_index {
    name            = "CountyIndex"
    hash_key        = "county"
    range_key       = "sk"
    projection_type = "ALL"
  }

  # TTL so items disappear ~5 minutes after arrival
  ttl {
    attribute_name = "expires_at" # Number: UNIX epoch seconds
    enabled        = true
  }

  tags = {
    Project = var.project_label
  }
}