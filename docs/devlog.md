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