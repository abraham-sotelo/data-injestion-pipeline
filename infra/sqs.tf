locals {
  resolved_sensor_queue_name = coalesce(var.sensor_queue_name, "${var.project_label}-sensor-data")
}

resource "aws_sqs_queue" "sensor_queue" {
  name                       = local.resolved_sensor_queue_name
  visibility_timeout_seconds = var.sensor_queue_visibility_timeout
  message_retention_seconds  = var.sensor_queue_retention_seconds
  delay_seconds              = var.sensor_queue_delay_seconds
  max_message_size           = var.sensor_queue_max_message_size
  receive_wait_time_seconds  = var.sensor_queue_receive_wait_seconds
  tags = {
    Project = var.project_label
  }
}

# Output the queue URL
output "sensor_queue_url" {
  value = aws_sqs_queue.sensor_queue.id
}