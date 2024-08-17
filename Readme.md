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
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/architecture.png" alt="architecture" width="50%">
