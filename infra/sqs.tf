resource "aws_sqs_queue" "sensor_queue" {
  name                       = "${var.project_label}-sensor-data"
  visibility_timeout_seconds = 30   # default time a msg is invisible to others when received
  message_retention_seconds  = 3600 # keep msgs 1 hour
  delay_seconds              = 0    # no delivery delay
  max_message_size           = 1024 # 1 KB
  receive_wait_time_seconds  = 1    # enable long polling (1s)
  tags = {
    Project = var.project_label
  }
}

# Output the queue URL
output "sensor_queue_url" {
  value = aws_sqs_queue.sensor_queue.id
}