# Lambda storing function
resource "aws_lambda_function" "storing" {
  function_name = "${var.project_label}-storing"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_storing.lambda_handler"
  runtime       = "python3.12"
  filename      = "lambda_storing.zip"
  source_code_hash = filebase64sha256("lambda_storing.zip")
  tags          = {Project = var.project_label}
}

#Lambda aggregate function
resource "aws_lambda_function" "aggregation" {
  function_name = "${var.project_label}-aggregation"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_aggregation.lambda_handler"
  runtime       = "python3.12"
  filename      = "lambda_aggregation.zip"
  source_code_hash = filebase64sha256("lambda_aggregation.zip")
  tags          = {Project = var.project_label}

  environment {
    variables = {
      RAW_TABLE       = aws_dynamodb_table.sensor_events.name
      AGGREGATE_TABLE = aws_dynamodb_table.county_aggregates.name
    }
  }
}


# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  tags = {Project = var.project_label}

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach basic execution policy to the Lambda role
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


# Mapping to trigger Lambda from SQS
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.sensor_queue.arn
  function_name    = aws_lambda_function.storing.arn
  batch_size       = 1
  enabled          = true
  tags             = {Project = var.project_label}
}


# IAM Policy to allow Lambda to read from SQS
resource "aws_iam_role_policy" "lambda_sqs" {
  name = "lambda_sqs_policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.sensor_queue.arn
      }
    ]
  })
}


# IAM Policy to allow Lambda to write to S3
# resource "aws_iam_role_policy" "lambda_s3" {
#   name = "lambda_s3_policy"
#   role = aws_iam_role.lambda_exec.id
#
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect   = "Allow"
#         Action   = ["s3:PutObject"]
#         Resource = "${aws_s3_bucket.data_bucket.arn}/*"
#       }
#     ]
#   })
# }


# IAM Policy to allow Lambda to write to DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name = "${var.project_label}-lambda-dynamodb-policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:UpdateItem"
        ],
        Resource = [
          aws_dynamodb_table.sensor_events.arn,
          aws_dynamodb_table.county_aggregates.arn
        ]
      }
    ]
  })
}


# EventBridge rule to trigger every minute
resource "aws_cloudwatch_event_rule" "every_minute" {
  name                = "run-aggregation-every-minute"
  schedule_expression = "rate(1 minute)"
  state               = "ENABLED"   # disable aggregator trigger
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_minute.name
  target_id = "aggregationLambda"
  arn       = aws_lambda_function.aggregation.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aggregation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_minute.arn
}