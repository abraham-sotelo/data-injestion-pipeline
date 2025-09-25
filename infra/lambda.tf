# Lambda function
resource "aws_lambda_function" "storing" {
  function_name = "storing_lambda"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  filename      = "lambda_function.zip"
  tags          = {Project = var.project_label}
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
resource "aws_iam_role_policy" "lambda_s3" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.data_bucket.arn}/*"
      }
    ]
  })
}


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
          "dynamodb:Scan"
        ],
        Resource = aws_dynamodb_table.sensor_events.arn
      }
    ]
  })
}