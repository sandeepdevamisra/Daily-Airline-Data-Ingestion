# Daily Airline Data Ingestion
## Objective
- Daily incremental data loading in AWS Redshift fact table
- As soon as file land in S3, we need to start the process
## Data
- Dimension table containing airport codes (airport_id, city, state, name). Pre-load it in Redshift.
- Daily flight data (Carrier, OriginAirportID, DestAirportID, DepDelay, ArrDelay). Will arrive daily in date-partitioned way.
- Target fact table (Carrier, Departure Airport, Arrival, Departure city, Arrival city, Departure State, Arrival State, Departure Delay, Arrival Delay). Will achieve through the ETL job. 
- Source of data:
  - https://www.kaggle.com/datasets/tylerx/flights-and-airports-data#airports.csv (aiport codes)
  - https://www.kaggle.com/tylerx/flights-and-airports-data#raw-flight-data.csv (daily flight data)
## Cloud Service
- AWS
## Techstacks
- S3
- S3 cloud trail notification
- Event Bridge Pattern rule
- Glue crawler
- Glue ETL
- SNS (for notification)
- Redshift (as warehouse)
- Step Function (for orchestration)
## Architecture
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/architecture.png" alt="architecture" width="80%">

## Steps
- Create an S3 bucket and create following folders inside it:
  - dims (upload the [airport code table](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/dimension_table/airports.csv) there.
  - daily_raw (where daily flight data will land up there partitioned by date)
  - bad_records (we will perform some quality check on the incoming raw date and those which fail to pass the check will land up here).
  - rule_outcome (part of quality check only)
  - temp (required for Redshift data ingestion)
- S3 dir structure:
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/s3_directory_structure.png" alt="architecture" width="30%">
- In Redshift create a schema for the dimension table and load the data from dims folder of S3 bucket.
  ```
  create schema airlines;

  CREATE TABLE airlines.airports_dim (
      airport_id BIGINT,
      city VARCHAR(100),
      state VARCHAR(100),
      name VARCHAR(200)
  );
  
  COPY airlines.airports_dim
  FROM '<enter S3 path to the file' 
  IAM_ROLE 'enter IAM role associated with Redshift'
  DELIMITER ','
  IGNOREHEADER 1
  REGION '<enter region of Redshift>';
  ```
  
- Similarly create a schema for the fact table (which will be loaded after the pipeline is finished).
  ```
  CREATE TABLE airlines.daily_flights_fact (
    carrier VARCHAR(10),
    dep_airport VARCHAR(200),
    arr_airport VARCHAR(200),
    dep_city VARCHAR(100),
    arr_city VARCHAR(100),
    dep_state VARCHAR(100),
    arr_state VARCHAR(100),
    dep_delay BIGINT,
    arr_delay BIGINT
   ```
  



