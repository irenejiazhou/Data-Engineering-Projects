# Overview
The goal of this project is to perform a thorough analysis and consistent monitoring of the distribution of COVID-19, as well as the associated medical resources.

This repository contains scripts, notebooks, and resources used to analyze the following specific research questions:

- <b> Descriptive Analysis:</b> What is the distribution of COVID-19 cases in the United States and the World? 

- <b> Causal & Predictive Analysis:</b> What are the factors that may cause the spread of COVID-19? 

By analyzing historical data, this project aims to identify trends and changes in these parameters over time. This will provide a comprehensive understanding of the spread of the virus and can provide insights into how to prevent group infections in the future from a public health perspective.

# Data Source
- [AWS - A public data lake for COVID-19 research and development](https://aws.amazon.com/covid-19-data-lake/)
  - AWS provides a public data lake with 39 raw tables sourced from 10+ contributors.
  - The data is formatted as <b>JSON</b> and <b>CSV</b> files.
  - Primary entities in this dataset
    - Demographics: Country, State, County
    - Time Unit: Date, Week, Month, Year
    - Vaccination
    - Hospital Bed
    - COVID-19 Tracing System User
    - COVID-19 Test Case
- I have also constructed a <b>data dictionary</b>, available here:

  [`covid_19_db_data_dictionary.xlsx`](https://github.com/irenejiazhou/Data-Engineering-Projects-Public/blob/main/COVID_ETL_Project/covid_19_db_data_dictionary.xlsx), which collates the metadata from the raw data.

# ELT Overview
<img src="https://github.com/irenejiazhou/Data-Engineering-Projects-Public/blob/main/COVID_ETL_Project/images/covid_etl.jpeg"  width="90%" height="90%">

- Extract
- Load
- Transform


# Data Warehouse Layers

- ODS (Operational Data Store)

  This layer stores the raw tables that are extracted from the AWS public S3 bucket.

- EDW (Enterprise Data Warehouse)
  - DWD (Data Warehouse Detail)

    This layer holds the data that has been essentially processed from the ODS layer, which includes operations such as cleaning, filtering, etc. The data is structured with a star schema and contains two types of tables: fact and dimension tables.

  - DWS (Data Warehouse Service)
    
    This layer houses the data that has been aggregated from the DWD layer.
    
- ADS (Application Data Store)

  This layer acts as a mapping of result tables in the EDW layer.

# Data Processing Rules



# Troubleshooting Highlights










# References
[Flink Is Attempting to Build a Data Warehouse Simply by Using a Set of SQL Statements](https://alibaba-cloud.medium.com/flink-is-attempting-to-build-a-data-warehouse-simply-by-using-a-set-of-sql-statements-57757badbb3f)

