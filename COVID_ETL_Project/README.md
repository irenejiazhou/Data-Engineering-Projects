# Overview
The goal of this project is to perform a thorough analysis and consistent monitoring of the distribution of COVID-19, as well as the associated medical resources.

This repository contains scripts, notebooks, and resources used to analyze the following specific research questions:

- <b> Descriptive Analysis:</b> What is the distribution of COVID-19 cases in the United States? 

- <b> Causal & Predictive Analysis:</b> What are the factors that may cause the spread of COVID-19? 

By analyzing historical data, this project aims to identify trends and changes in these parameters over time. This will provide a comprehensive understanding of the spread of the virus and can provide insights into how to prevent group infections in the future from a public health perspective.

# Data Source
- [AWS - A public data lake for COVID-19 research and development](https://aws.amazon.com/covid-19-data-lake/)
  - AWS provides a public data lake with 39 raw tables sourced from 10+ contributors.
  - The data is formatted as <b>JSON</b> and <b>CSV</b> files.
  - Primary entities in this dataset
    - Demographics: State, City, County
    - Time Unit: Date, Week, Month, Year
    - Vaccination
    - Hospital
    - COVID-19 Tracing System User
    - COVID-19 Test Case
- I have also constructed a <b>data dictionary</b>, available here:

  [`covid_19_db_data_dictionary.xlsx`](https://github.com/irenejiazhou/Data-Engineering-Projects-Public/blob/main/COVID_ETL_Project/covid_19_db_data_dictionary.xlsx), which collates the metadata from the raw data.
- For the covidcast_data table, the official data dictionary document is [here](https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/hhs.html)

# ELT Overview
<img src="https://github.com/irenejiazhou/Data-Engineering-Projects-Public/blob/main/COVID_ETL_Project/images/covid_etl.jpeg"  width="90%" height="90%">

- Extract
- Load
- Transform


# Data Warehouse Layers

- <b>ODS (Operational Data Store)</b>

  This layer stores the raw tables that are extracted from the AWS public S3 bucket.

- <b>EDW (Enterprise Data Warehouse)</b>
  - <b>DWD (Data Warehouse Detail)</b>
    - This layer holds the data that has been essentially processed from the ODS layer, which includes operations such as cleaning, filtering, etc. The data is structured with a star schema and contains two types of tables: fact and dimension tables.

    - Processing Rules

      1. Clean the format of times
      2. zipcode starting with 0 is missing the first digit because the data type is num.
      3. TBD...
    

  - <b>DWS (Data Warehouse Service)</b>
    
    This layer houses the data that has been aggregated from the DWD layer.
    
- <b>ADS (Application Data Store)</b>

  This layer acts as a mapping of result tables in the EDW layer.


# Troubleshooting Highlights

1. When connecting to Redshift, we need to make sure that:

   - Cluster: `Network and security settings` -> `Publicly accessible` -> `Enabled`
   - VPC dashboard: `Security` -> `Security groups` -> `Inbound rules` -> `Edit inbound rules` -> `Add rule`
     - If we use <b>online platforms</b> like Databricks to run the Jupiter notebook,
       - Type: Redshift
       - Protocol: TCP
       - Port Range: 5439
       - Source: Anywhere-IPv4
     - If we use a <b>local machine</b> to run it,
       - Type: Redshift
       - Protocol: TCP
       - Port Range: 5439
       - Source: My IP 

2. Check If the Extraction Query from Athena is Finished (1.4.1 in [`part_1_covid_etl_full_project.ipynb`](https://github.com/irenejiazhou/Data-Engineering-Projects-Public/blob/main/COVID_ETL_Project/part_1_covid_etl_full_project.ipynb))

   The following query is executed ASYNCHRONOUSLY.
   ```
   query_cdc_moderna_vaccine_distribution = athena_client.start_query_execution(
    QueryString = 'SELECT * FROM cdc_moderna_vaccine_distribution',
    QueryExecutionContext = {'Database': athena_db_name},
    ResultConfiguration = { 
        'OutputLocation': s3_raw_data_dir,
        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}})
   ```

   <b>ASYNCHRONOUSLY</b> means if the task takes a long time, the start_query_execution method will start the task and then continue to run the rest of this Jupyter notebook, which means even if the query is not completed, the script on Jupyter Notebook still shows it is executed successfully. The following script checks if the query is successfully executed, succeed, running, or failed. If not, what's the error type?
    ```
    # Retrieve the QueryExecutionId from the response of the start_query_execution method
    query_execution_id = query_world_cases_deaths_testing['QueryExecutionId']
    # Get the query execution details
    query_execution = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
    # If the query execution status is 'FAILED', print the error message
    if query_execution['QueryExecution']['Status']['State'] == 'FAILED':
        print('Query failed with the following error:')
        print(query_execution['QueryExecution']['Status']['StateChangeReason'])
    else:
        print('Query status:', query_execution['QueryExecution']['Status']['State'])
    ```
    
# References
[Flink Is Attempting to Build a Data Warehouse Simply by Using a Set of SQL Statements](https://alibaba-cloud.medium.com/flink-is-attempting-to-build-a-data-warehouse-simply-by-using-a-set-of-sql-statements-57757badbb3f)

