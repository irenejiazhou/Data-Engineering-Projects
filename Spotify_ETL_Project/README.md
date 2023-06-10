# Music Data Pipeline

This project is an implementation of a data pipeline to collect and store music data from the Spotify API. The aim is to gather data about songs, albums, and artists to conduct a deep analysis and get insights into the music trends and preferences.

## Overview

The data pipeline architecture is based on [Darshil's work](https://github.com/darshilparmar/python-for-data-engineering/tree/main/6.%20End-To-End%20Data%20Pipeline%20Project), but it has been adjusted according to my professional experience with data warehouse design. The core steps include data extraction from Spotify API and data transformation.

## Project Structure

- `main.py`: The main driver script that coordinates the execution of the pipeline.
- `data_extraction.py`: This script handles the data extraction process from the Spotify API.
- `data_transformation.py`: This script is used to transform the data into a suitable format for the data warehouse.
- `data_loading.py`: This script loads the transformed data into the data warehouse.

## Setup & Execution

To run this project, you would need to:

1. Install the required Python packages: 
    ```
    pip install -r requirements.txt
    ```
2. Update the `config.py` with your Spotify API credentials and database details.
3. Run the main script:
    ```
    python main.py
    ```
Enjoy the Music data journey!
