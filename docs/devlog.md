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

## 5. End-to-End Testing
The E2E test will stream sample data through the ingestion pipeline and then query the aggregate table to confirm the data was processed correctly.  

### Strategy
1. **Produce fresh events**  
   The test runs `producer.py` with a fixed `--limit` to stream a known number of samples into the pipeline.

2. **Trigger aggregation Lambda**  
   The aggregator is invoked directly (bypassing the scheduled run) with a unique `test_run_id`.  
   This ensures the test queries only the aggregate row created by this run.

3. **Query aggregate table**  
   The test fetches the row tagged with `test_run_id` and records its `updated` timestamp.

4. **Recompute locally**  
   Using the same 5-minute window ending at `updated`, the test queries the sensor data table and counts events per county.

5. **Compare results**  
   The locally computed totals and per-county counts are compared with the DynamoDB aggregate row.  
   Any mismatch causes the test to fail with a clear diagnostic message.