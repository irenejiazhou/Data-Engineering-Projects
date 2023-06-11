# Spotify API Music Data Pipeline Using AWS

## Business Requirements
This project is an implementation of a data pipeline to collect and store music data from the Spotify API. The aim is to gather data about songs, albums, and artists to conduct a deep analysis and get insights into the music trends and preferences.
The data pipeline architecture is based on [Darshil's work](https://github.com/darshilparmar/python-for-data-engineering/tree/main/6.%20End-To-End%20Data%20Pipeline%20Project), but it has been adjusted according to my professional experience with data warehouse design. The core steps include data extraction from Spotify API and data transformation.

## ETL Architecture


- Data Ingestion: [Spotify API](https://developer.spotify.com/dashboard)

  `Redirect URIs: http://localhost:3000.`

- Data Extract: [Python - Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)




## Data Source
[Spotify - Top Song - Global "Your <b>WEEKLY</b> update of the most played tracks right now."](https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF)
<br>
<img src="https://github.com/irenejiazhou/Data-Engineering-Projects/blob/main/Spotify_ETL_Project/Others/Spotify_Top_Songs_Global.png"  width="40%" height="40%">



Update Frequency:
数据量
domains
获取机制： on-demand
加载方式：全量、增量
取数逻辑



## Dashboard

## Key Metrics



- [`ETL_Project_Spotify_API.ipynb`](https://github.com/irenejiazhou/Data-Engineering-Projects/blob/main/Spotify_ETL_Project/ETL_Project_Spotify_API.ipynb): The main driver script that coordinates the execution of the pipeline.
- `data_extraction.py`: This script handles the data extraction process from the Spotify API.

## Project Highlights

To run this project, you would need to:

1. Create an app in Spotify Developer Dashboard.

1. Install the required Python packages: 
    ```
    pip install -r requirements.txt
    ```

