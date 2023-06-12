# Spotify API Music Data Pipeline Using AWS

## Business Requirements
This project is an implementation of a data pipeline to collect and store music data from the Spotify API. The aim is to gather data about songs, albums, and artists to conduct a deep analysis and get insights into the music trends and preferences.
The data pipeline architecture is based on [Darshil's work](https://github.com/darshilparmar/python-for-data-engineering/tree/main/6.%20End-To-End%20Data%20Pipeline%20Project), but it has been adjusted according to my professional experience with data modeling design. 

## Data Source
<img src="https://github.com/irenejiazhou/Data-Engineering-Projects/blob/main/Spotify_ETL_Project/Others/Spotify_Top_Songs_Global.png"  width="30%" height="30%">

[Spotify - Top Song - Global "Your <b>WEEKLY</b> update of the most played tracks right now."](https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF)

| Update Info             | Details             |
| :---------------------- | :------------------ |
| <b>Update Frequency</b> | Weekly              |
| <b>Amount of Data</b>   | 50 Rows             |
| <b>Domains</b>          | Song, Album, Artist |
| <b>Loading Method</b>   | Full Load           |
| <b>Partitioning</b>     | Year & Week         |


## ETL Architecture
- [<b>Spotify API</b>](https://developer.spotify.com/dashboard)
  - `Redirect URIs: http://localhost:3000.`

- <b>AWS Lambda</b>
  - <b>Functions</b>
  <br> Python is employed to perform preliminary processing on the semi-structured raw data to convert it into structured data.
  - [<b>Python - Spotipy</b>](https://spotipy.readthedocs.io/en/2.22.1/)
  <br> The Spotipy library is incorporated into a Lambda layer for fetching data from the Spotify API.
 
- <b>AWS S3</b>
<br> Serves as a data lake for storing raw data as JSON files and processed data as CSV files. 

- <b>AWS Glue-Data Catalog</b>
<br> Provides a database for storing processed tables.
  - <b>Crawler</b>
  <br> Scheduled to update the database with the latest processed data from S3 on a weekly basis.
    - Update Schedule: Every Monday at 10 PM
  
- <b>Amazon Athena</b>
<br> Allows inspection of the schema and validation of data quality in the tables loaded into the database.

- <b>CloudWatch Trigger</b>
<br> Scheduled to activate the `spotify_api_data_extract` Lambda function weekly, fetching data from the Spotify API.
  - Update Schedule: Every Monday at 10 AM `cron(0 10 ? * MON *)` 

- <b>Lambda Trigger</b>
<br> Set to trigger the `spotify_transformation_load` Lambda function immediately after the execution of the extraction Lambda function.

## Database Design


## Project Structure

- [`ETL_Project_Spotify_API.ipynb`](https://github.com/irenejiazhou/Data-Engineering-Projects/blob/main/Spotify_ETL_Project/ETL_Project_Spotify_API.ipynb): The main driver script that coordinates the execution of the pipeline.
- `data_extraction.py`: This script handles the data extraction process from the Spotify API.

## Data Processing Highlights

- Problem: The column names of song_artist_data and artist tables are not recognized by the crawler.
  1. Rename Field Names: `AWS Glue -> Tables -> song_artist_data -> Edit schema as JSON`
  2. Skip the First Row: `AWS Glue -> Tables -> song_artist_data -> Actions -> Edit Table -> Table Properties`

      | Key                    | Value |
      | :--------------------- | :---- |
      | skip.header.line.count | 1     |

- Problem: There are album and song names contains `,`, which means there will be bugs when use `,` as delimiter in the csv files.
  1. Search possible delimiters in the raw JSON file, and `;` doesn't appear.
  2. Change the delimiter from `,` to `;`
  
      ```
      song_buffer = StringIO() # CREATE AN IN-MEMORY BUFFER where the CSV file can be written.
      song_df.to_csv(song_buffer, sep = ';', index = False) # No index col for the result table
      ```
