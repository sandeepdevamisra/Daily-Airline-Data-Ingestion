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

## Flow
- Create an S3 bucket and create following folders inside it:
  - dims (upload the [airport code table](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/dimension_table/airports.csv) there.
  - daily_raw (where daily flight data will land up there partitioned by date)
  - bad_records (we will perform some quality check on the incoming raw date and those which fail to pass the check will land up here).
  - rule_outcome (part of quality check only)
  - temp (required for Redshift data ingestion)
- S3 dir structure
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/s3_directory_structure.png" alt="architecture" width="50%">
  


