# Challenge Statement

This challenge is about creating a sensor data collection pipeline using AWS managed services.

## Details

Architect and create a real-time ingestion pipeline for sensor data collection.

1. Data: use the Recommended-Fishing-Rivers-And-Streams dataset.  
  *Please make sure to download the file in CSV format.  
  a. State of New York - Recommended Fishing Rivers And Streams

2. Architecture  
  a. Architect the real-time ingestion pipeline using AWS managed services and draw an architecture diagram to elucidate your design.

3. Implementation:  
  a. Write an application that uploads the dataset data to the ingestion pipeline. This application should add a timestamp column to the data and should publish at least 10 rows per second  
  b. Implement an aggregation of the County field for the last 5 minutes.

4. Testing  
  a. Include unit tests for the application  
  b. Include end to end tests that confirm data gets persisted.

5. Deployment  
  a. Define the infrastructure for your pipeline using infrastructure as code tools, such as CloudFormation or Terraform.  
  b. Provide bash scripts called build.sh, unit_test.sh, deploy.sh and stream.sh  
    i. build.sh builds the application  
    ii.  unit_test.sh runs the unit tests for the application  
    iii.  deploy.sh creates the infrastructure defined in 5a.  
    iv.  stream.sh runs the application and streams data indefinitely.
    
    
    

## What to return back to us

1. Please zip everything in a directory named yourfirstname.lastname/ and return via email.  
2. Please make sure we can see your git commit history.  
3. Please include a README.md file that documents your project as best as you can so we know what it does and how to run it.  
4. In your email response please let us know roughly how many hours you spent on this exercise.
