import pandas as pd
import requests
import re
from io import StringIO

DATASET_URL = "https://github.com/JCMiriam/mood_tune_back/raw/refs/heads/main/src/data/final_df.csv"

df_dataset = None

def load_dataset():
    """Carga el dataset desde GitHub si aún no está en memoria."""
    global df_dataset
    if df_dataset is None:
        response = requests.get(DATASET_URL)
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            df_dataset = pd.read_csv(csv_data)
        else:
            raise Exception("Error al cargar el dataset")
    return df_dataset

def normalize_string(text):
    if not isinstance(text, str):
        return text
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def check_songs_in_dataset(user_songs):
    global df_dataset
    if df_dataset is None:
        df_dataset = load_dataset() 

    dataset_songs = df_dataset[["song_name", "artist_name", "track_uri", "spotify_url"]].copy()
    dataset_songs = dataset_songs.applymap(normalize_string)

    matching_songs = []

    for song in user_songs:
        song_name = normalize_string(song.get("name", ""))
        artist_name = normalize_string(song.get("artists", [{}])[0].get("name", ""))
        track_uri = normalize_string(song.get("uri", ""))
        spotify_url = normalize_string(song.get("external_urls", {}).get("spotify", ""))

        match = dataset_songs[
            (dataset_songs["track_uri"] == track_uri) |
            (dataset_songs["spotify_url"] == spotify_url) |
            ((dataset_songs["song_name"] == song_name) & (dataset_songs["artist_name"] == artist_name))
        ]

        if not match.empty:
            matching_songs.append(song)

    return matching_songs

def check_artists_in_dataset(user_artists):
    global df_dataset
    if df_dataset is None:
        df_dataset = load_dataset() 

    dataset_artists = set(df_dataset["artist_name"].apply(normalize_string))

    matching_artists = [artist for artist in user_artists if normalize_string(artist["name"]) in dataset_artists]

    return matching_artists
