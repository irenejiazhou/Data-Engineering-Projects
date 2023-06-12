import json
import boto3
from datetime import datetime
from io import StringIO # for csv file convert
import pandas as pd

def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id': album_id, 
                         'album_name': album_name,
                         'album_release_date': album_release_date, 
                         'album_total_tracks': album_total_tracks,
                         'album_url': album_url}
        album_list.append(album_element)
    return album_list

def artist(data):
    artist_list = []
    for row in data['items']:
        for key,value in row.items():
            if key == 'track':
                artists = []
                for artist in value ['artists']: 
                    # Note: One song can have multiple artists
                    # Tag artists is a list with each element as an sigle artist.
                    artist_element = {'artist_id': artist['id'],
                                      'artist_name': artist['name'],
                                      'external_url': artist['href']}
                    artist_list.append(artist_element)
    return artist_list

def song(data):
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added_time = row['added_at']
        album_id = row['track']['album']['id']
        artist_id_1st = row['track']['artists'][0]['id']
        # artists_list = [artist['id'] for artist in row['track']['artists']]
        song_element = {'song_id': song_id,
                        'song_name': song_name,
                        'song_duration': song_duration,
                        'song_url': song_url,
                        'song_popularity': song_popularity,
                        'song_added_time': song_added_time,
                        'album_id': album_id
                        # 'artist_id_1st': artist_id_1st,
                        # 'artists_list': artists_list
                        }
        song_list.append(song_element)
    return song_list

def song_artist_mapping(data):
    song_artist_mapping_tbl = []
    for row in data['items']:
        song_id = row['track']['id']
        # song_name = row['track']['name']
        # Creat a list of all artists for each song
        for artist in row['track']['artists']:
            artist_id = artist['id']
            # artist_name = artist['name']
            # Creat a mapping record for each combination of artist and song
            song_artist_mapping_tbl.append({'song_id': song_id,
                                            'artist_id': artist_id})
    return song_artist_mapping_tbl


def lambda_handler(event, context):
    # Extract files from to_processed folder, which are stored to the folder in the api_extract function
    
    # Creating an S3 client with boto3 which provides a set of methods to interact with S3.
    s3_client = boto3.client('s3')
    Bucket = 'spotify-etl-project-irene'
    Key = 'raw_data/to_processed/' # Key folder
    
    spotify_data = []
    spotify_keys = []
    
    # Check all files in the key folder
    for file in s3_client.list_objects(Bucket = Bucket, Prefix = Key)['Contents']:
        # print(file['Key']) # List out all files in the key folder path
        file_key = file['Key'] # the list of file keys (names)
        # If the file is json:
        if file_key.split('.')[-1] == 'json':
            response = s3_client.get_object(Bucket = Bucket, Key = file_key) 
            content = response['Body'] # Return value <botocore.response.StreamingBody object at 0x7f66866eb520>, which is under key 'Body'
            json_object = json.loads(content.read()) # read the file and use json.load() to transfer it to python dictionary
            spotify_data.append(json_object) # put all dictionaries in a list
            spotify_keys.append(file_key) # put all file paths of the json files in to_processed folder
            
    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = song(data)
        song_artist_mapping_tbl = song_artist_mapping(data)
        
        album_df = pd.DataFrame.from_dict(album_list)
        artist_df = pd.DataFrame.from_dict(artist_list)
        song_df = pd.DataFrame.from_dict(song_list)
        song_artist_df = pd.DataFrame.from_dict(song_artist_mapping_tbl)
        
        album_df = album_df.drop_duplicates(subset=['album_id'])
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])
        song_df = song_df.drop_duplicates(subset=['song_id'])
        song_artist_df = song_artist_df.drop_duplicates(subset=['song_id', 'artist_id'])
        
        album_df['album_release_date'] = pd.to_datetime(album_df['album_release_date'])
        song_df['song_added_time'] = pd.to_datetime(song_df['song_added_time'])
        
        # 获取当前年和月
        current_year = str(datetime.now().year)
        current_month = str(datetime.now().month)

        song_key = 'transformed_data/song_data/' + current_year + '/' + current_month + '/' + 'song_transformed_' + str(datetime.now()) + '.csv'
        song_buffer = StringIO() # CREATE AN IN-MEMORY BUFFER where the CSV file can be written.
        song_df.to_csv(song_buffer, sep=';', index=False)
        song_content = song_buffer.getvalue() # FETCH all the data (the content of the CSV file) from the StringIO buffer.
        s3_client.put_object(Bucket = Bucket, Key = song_key, Body = song_content) # # UPLOAD the CSV file from the StringIO buffer to S3.
        
        album_key = 'transformed_data/album_data/' + current_year + '/' + current_month + '/' + 'album_transformed_' + str(datetime.now()) + '.csv'
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, sep=';', index=False)
        album_content = album_buffer.getvalue() 
        s3_client.put_object(Bucket = Bucket, Key = album_key, Body = album_content)
        
        artist_key = 'transformed_data/artist_data/' + current_year + '/' + current_month + '/' + 'artist_transformed_' + str(datetime.now()) + '.csv'
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, sep=';', index=False)
        artist_content = artist_buffer.getvalue()
        s3_client.put_object(Bucket = Bucket, Key = artist_key, Body = artist_content) 
        
        song_artist_key = 'transformed_data/song_artist_data/' + current_year + '/' + current_month + '/' + 'song_artist_transformed_' + str(datetime.now()) + '.csv'
        song_artist_buffer = StringIO()
        song_artist_df.to_csv(song_artist_buffer, sep=';', index=False)
        song_artist_content = song_artist_buffer.getvalue()
        s3_client.put_object(Bucket = Bucket, Key = song_artist_key, Body = song_artist_content) 
        
        # StringIO(): A class that allows for reading and writing of strings in memory. 
        #             Its primary use is to store strings in memory like a file. 

        # getvalue(): A method of the StringIO object. 
        #             It returns all the data that has been written into the StringIO object. 

        # put_object(): A function in the boto3 library used for uploading an object to Amazon S3. 
        #               bucket name (Bucket), key (Key, which is the path of the file in S3), and Body (the data to be uploaded). 
        
        # Copy files in to_processed folder to processed folder
        # 1. Create an Amazon S3 resource object which is a higher-level, object-oriented API compared to a client. 
        s3_resource = boto3.resource('s3')
        for file_key in spotify_keys:
            copy_file_keys = {
                'Bucket': Bucket,
                'Key': file_key
            }
            # Copy the file to processed folder
            s3_resource.meta.client.copy(copy_file_keys, Bucket, 'raw_data/processed/' + file_key.split('/')[-1]) # split() get the file name from file path (key)
            # copy(CopySource, Bucket, Key, ExtraArgs=None, Callback=None, SourceClient=None, Config=None)
            # CopySource is a dictionary：{'Bucket': 'bucket', 'Key': 'key', 'VersionId': 'id'}。
            # Bucket (str) is the destination bucket
            # Key (str) is the destination file name
            
            
            # Delete files in the to_processed folder
            s3_resource.Object(Bucket, file_key).delete()
            # Since this for loop deleted all files under to_processed, the to_processed folder is automatically deleted.
        
        
