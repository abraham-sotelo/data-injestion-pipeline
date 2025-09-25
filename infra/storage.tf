# S3 bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_label}-sensor-data-12345"
  tags   = {Project = var.project_label}
}