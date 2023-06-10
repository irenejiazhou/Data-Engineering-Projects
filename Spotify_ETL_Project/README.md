# Spotify API Music Data Pipeline Using AWS

This project is an implementation of a data pipeline to collect and store music data from the Spotify API. The aim is to gather data about songs, albums, and artists to conduct a deep analysis and get insights into the music trends and preferences.

## Overview

The data pipeline architecture is based on [Darshil's work](https://github.com/darshilparmar/python-for-data-engineering/tree/main/6.%20End-To-End%20Data%20Pipeline%20Project), but it has been adjusted according to my professional experience with data warehouse design. The core steps include data extraction from Spotify API and data transformation.

## Business Requirement

## Data Source
[Top Song - Global](https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF)
<img src="Spotify_ETL_Project/Others/Spotify_Top_Songs_Global.png"  width="600" height="300">


## ETL Architecture
image here

## Dashboard
image here 

## Metrics Monitored

## Project Structure

- [`ETL_Project_Spotify_API.ipynb`](https://github.com/irenejiazhou/Data-Engineering-Projects/blob/main/Spotify_ETL_Project/ETL_Project_Spotify_API.ipynb): The main driver script that coordinates the execution of the pipeline.
- `data_extraction.py`: This script handles the data extraction process from the Spotify API.

## Detailed Explanation

To run this project, you would need to:

1. Install the required Python packages: 
    ```
    pip install -r requirements.txt
    ```

