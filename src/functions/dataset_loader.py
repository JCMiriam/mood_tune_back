import pandas as pd
import requests
from io import StringIO

DATASET_URL = "https://github.com/JCMiriam/mood_tune_back/raw/refs/heads/main/src/data/final_df.csv"

df_dataset = None

def load_dataset():
    global df_dataset
    if df_dataset is None:
        response = requests.get(DATASET_URL)
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            df_dataset = pd.read_csv(csv_data)
        else:
            raise Exception("Error on load dataset")
    return df_dataset

def check_songs_in_dataset(user_songs):
    global df_dataset
    if df_dataset is None:
        df_dataset = load_dataset() 

    dataset_songs = df_dataset[["song_name", "artist_name", "track_uri", "spotify_url"]].copy()
    dataset_songs = dataset_songs.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    matching_songs = []

    for song in user_songs:
        song_name = song.get("name", "").lower()
        artist_name = song.get("artists", [{}])[0].get("name", "").lower()
        track_uri = song.get("uri", "").lower()
        spotify_url = song.get("external_urls", {}).get("spotify", "").lower()

        match = dataset_songs[
            (dataset_songs["track_uri"] == track_uri) |
            (dataset_songs["spotify_url"] == spotify_url) |
            ((dataset_songs["song_name"] == song_name) & (dataset_songs["artist_name"] == artist_name))
        ]

        if not match.empty:
            matching_songs.append(song)

    return matching_songs