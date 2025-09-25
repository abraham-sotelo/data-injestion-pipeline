# Development Log

## 1. Data Format Choice
I chose **JSON** for simplicity of processing.
- Easier to extend and process during aggregation.
- Increases overhead compared to raw CSV (slightly larger payloads).
- If time remains, I can optimize to **CSV** to reduce the traffic.

## 2. Use of AWS Free Tier Resources
I decided to prioritize AWS Free Tier resources for this challenge.
- Keeps the setup cost-free while still showcasing the pipeline design.
- Simplifies testing and avoids billing surprises.

## 3. Storage Choice: DynamoDB over S3
I selected **DynamoDB** as the storage instead of **S3 buckets**.
- DynamoDB offers fast lookups and updates, which simplifies real-time aggregation.
- S3 is better for raw archival but less efficient for frequent small writes.
- Easier to query and maintain rolling aggregates in DynamoDB.
- Slightly higher complexity in schema design compared to S3.

## 4. Aggregation Strategy
I will implement the 5-minute County aggregation in a **Lambda function** that updates a DynamoDB table.
- Keeps the aggregation logic serverless, lightweight, and easy to test.
- DynamoDB supports efficient updates and queries without additional infrastructure.
- Suitable for the challenge scale, but for higher throughput, a streaming service (e.g., Kinesis, Flink) may be required.
