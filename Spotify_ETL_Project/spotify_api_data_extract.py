import json
import os  # To import the cliend_id and client_secret stored in the configuration/evironment variables which is for security concern
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 # To Store the JSON file from Spotify API to S3
from datetime import datetime

def lambda_handler(event, context):
    
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    # API Authentication
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    # API Authorization: Permission to Access Data from Spotify API
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'
    playlist_URI = playlist_link.split("/")[-1] # To Get '37i9dQZEVXbNG2KDcFcKOF''
     
    spotify_raw_data = sp.playlist_tracks(playlist_URI)
    # print(spotify_raw_data)
    
    client = boto3.client('s3')
    
    # Create the Destination File Name
    file_name = 'spotify_raw_data_' + str(datetime.now()) + '.json'
    
    # Add extracted raw data to to_processed 
    client.put_object(
        Bucket = 'spotify-etl-project-irene',
        Key = 'raw_data/to_processed/' + file_name,
        Body = json.dumps(spotify_raw_data)) # json.dumps() means converting into JSON format