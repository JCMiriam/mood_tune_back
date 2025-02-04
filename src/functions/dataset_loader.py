import pandas as pd
import re
from rapidfuzz import fuzz, process

DATASET_PATH = "C:/Users/USUARIO/Desktop/Projects/mood_tune_back/src/data/final_df.csv"
df_dataset = None

def load_dataset():
    global df_dataset
    if df_dataset is None:
        df_dataset = pd.read_csv(
            DATASET_PATH,
            usecols=["song_name", "artist_name"],
            dtype=str
        )
        df_dataset = df_dataset.dropna(subset=["song_name", "artist_name"])
        df_dataset["song_name"] = df_dataset["song_name"].apply(normalize_string)
        df_dataset["artist_name"] = df_dataset["artist_name"].apply(normalize_string)
    return df_dataset

def normalize_string(text):
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def check_songs_in_dataset(user_songs, threshold=75):
    df_dataset = load_dataset()

    dataset_song_artist = df_dataset.apply(lambda row: f"{row['song_name']} {row['artist_name']}", axis=1).tolist()

    matching_songs = []
    for song in user_songs:
        if "name" not in song or "artists" not in song:
            continue 

        song_name = normalize_string(song.get("name", ""))
        artist_name = normalize_string(song["artists"][0].get("name", ""))
        song_query = f"{song_name} {artist_name}"

        best_match, score, _ = process.extractOne(song_query, dataset_song_artist, scorer=fuzz.ratio)

        print(f"🔍 Comparando: '{song_query}' → Mejor coincidencia: '{best_match}' (Similitud: {score}%)")  # 🔥 Debug

        if score >= threshold:
            matching_songs.append(song)

    return matching_songs


def check_artists_in_dataset(user_artists, threshold=75):
    df_dataset = load_dataset()

    dataset_artists = df_dataset["artist_name"].tolist()

    matching_artists = []
    for artist in user_artists:
        artist_name = normalize_string(artist.get("name", ""))

        best_match, score, _ = process.extractOne(artist_name, dataset_artists, scorer=fuzz.ratio)

        print(f"Comparando artista: '{artist_name}' → Mejor coincidencia: '{best_match}' (Similitud: {score}%)")

        if score >= threshold:
            matching_artists.append(artist)

    return matching_artists
