# S3 bucket
#resource "aws_s3_bucket" "data_bucket" {
#  bucket = "${var.project_label}-sensor-data-12345"
#  tags   = {Project = var.project_label}
#}


# DynamoDB table to store raw events for last-5-minute window
resource "aws_dynamodb_table" "sensor_events" {
  name         = "${var.project_label}-sensor-events"
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

  tags = {
    Project = var.project_label
  }
}



# 2. DynamoDB Aggregates table
resource "aws_dynamodb_table" "county_aggregates" {
  name         = "${var.project_label}-county_aggregates"
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
