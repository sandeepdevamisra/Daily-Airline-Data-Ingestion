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

## File strucuture
- `Daily_Airline_Data_Ingestion/`
  - `dimension_table/`
    - `airpors.csv`
  - `airline_data/`
    - `date=2024-04-06/`
      - `flights.csv`
  - `airline_data_archive/`
  - `img/`
  - `event_pattern_stepfunction.json`
  - `event_pattern_dataquality.json`
  - `s3_file_upload.py`
  - `Readme.md`

## Steps
- Create an S3 bucket and create following folders inside it:
  - dims (upload the [airport code table](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/dimension_table/airports.csv) there.
  - daily_raw (where daily flight data will land up there partitioned by date)
  - rule_outcome (we will perform some quality check on the incoming raw data and the result of the evaluation will land up here). 
  - bad_records (all those records which fail the quality check will land up here).
  - temp (required for Redshift data ingestion)
- S3 dir structure:
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/s3_directory_structure.png" alt="architecture" width="30%">

- In Redshift create a schema and then the the dimension table and load the data from dims folder of S3 bucket.

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

  
- Similarly create a the fact table (which will be loaded after the pipeline is finished).

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
- Run the Glue crawler on both the the tables. This is an one-time activity. For the incoming data in S3, we will have to run the crawler everytime, and therefore, we will automate the process using Step Function. 
- Given that both the Glue ETL Job and Step Function are set up, to automate the entire process such that as soon as the data lands in S3 the Step Function is triggered, create a CloudTrail trail in the S3 bucket. Enable cloudwatch log as well. After this, create an [Event Bridge rule](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/event_pattern_stepfunction.json) where source is S3, target is Step Function, event type is AWS API call via CloudTrail and the suffix is "/flights.csv".
## Run instructions
- In the local keep 2 directories, [airline_data](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/tree/main/airline_data) which will contain the raw data in date partitioned way (data for 2024-04-06 should be stored in a directory with name `date=2024-04-06`) and [airline_data_archive](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/tree/main/airline_data_archive) which will be initially empty but when we move the data to S3, the raw data will be stored in this directory and removed from the original directory to avoid duplicate entries in future.
- Run the command `python3 s3_file_upload.py`
- After the command finishes executing, any new raw data will be moved to S3 bucket and a local copy will be stored in the archive folder. As soon as data lands in S3 bucket, Step Function will be triggered and after some time data will be available in Redshift. 

## Glue ETL Job
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/glue_etl.png" alt="glue etl" width="80%">

- Perform data quality check on the raw data for missing values in columns like arrival and departure airport codes, carrier, and check for range of airport codes. These records will be published to CloudWatch log such that later we can create Event Bridge rule so that we can trigger an SNS notification after the quality check is done.
- The result of the quality check will land on the `rule_outcome` folder in S3 bucket. This way we can later analyse the quality of our raw data.
- Also, apply the quality check record-wise. If a record fails, put it in the `bad_records` folder in S3 bucket. Those records which pass the check will be used as our final raw data. But before finalizing the raw data, remove additional columns which were added as a result of quality check.
- Since the quality check is set up, create an [Event Bridge rule](https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/event_pattern_dataquality.json) such that we can get SNS notification after the quality check is done. The event source should be Glue DataQuality, event type should be DataQuality Evaluation Results Available, event state should be Succeeded, Failer, and target should be SNS.
- Now we have the raw data ready. Perform inner join with the airport codes dimension table (that we pre-loaded) twice - first, for getting the departure airport information and, second, for getting the arrival airport information.
- Perform some schema changes since extra columns will be added while joining. The target should be Redshift.
- Enable job bookmark for incremental loading. 
## Step Function
<img src="https://github.com/sandeepdevamisra/Daily-Airline-Data-Ingestion/blob/main/img/step_function.png" alt="step function" width="60%">



