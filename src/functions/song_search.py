import numpy as np
import time
from deep_translator import GoogleTranslator
from langdetect import detect
from src.models.model_loader import model_data


def translate_to_english(text):
    """Traduce la frase del usuario a inglés si no está en inglés."""
    try:
        if text and isinstance(text, str) and text.strip():
            detected_lang = detect(text)
            if detected_lang != 'en':
                translated_text = GoogleTranslator(source='auto', target='en').translate(text)
                print(f"🌍 Traducido: '{text}' → '{translated_text}'")
                return translated_text
        return text
    except Exception as e:
        print(f"❌ Error detectando idioma: {e}")
        return text  # Si hay error, usa el texto original


# 📌 Importar datos pre-cargados
df = model_data["df"]
index = model_data["index"]
model = model_data["model"]

def search_songs(user_query, top_n=15):
    """
    Busca canciones en base a una frase del usuario usando FAISS.
    
    - user_query: Texto ingresado por el usuario.
    - top_n: Número de canciones recomendadas.
    """
    start_time = time.time()

    if df is None:
        print("❌ Error: El DataFrame de canciones no se ha cargado correctamente.")
        return [{"error": "El DataFrame de canciones no está disponible"}]

    # 📌 Traducir la consulta a inglés si es necesario
    translated_query = translate_to_english(user_query)

    # 📌 Convertir la consulta en embedding
    query_embedding = model.encode(translated_query, convert_to_tensor=True).cpu().numpy().astype('float32')

    # 📌 Buscar en FAISS
    distances, indices = index.search(np.array([query_embedding]), top_n)

    # 📌 Verificar si hay resultados
    if indices is None or indices.size == 0:
        print("❌ No se encontraron resultados.")
        return [{
            "artist_name": "Error",
            "song_name": "No se encontraron canciones",
            "spotify_url": "",
            "processed_lyrics": "No hay letra disponible",
            "translated_lyrics": "Traducción no disponible",
            "similarity": 0
        }]

    # 📌 Verificar que `df` contiene los índices correctos
    try:
        top_songs = df.iloc[indices[0]].copy()
    except Exception as e:
        print(f"❌ Error al recuperar canciones del DataFrame: {e}")
        return [{"error": "No se pudieron recuperar canciones"}]

    top_songs['similarity'] = 1 - distances[0]  # Convertir distancia en similitud

    # 📌 Filtrar canciones inválidas
    top_songs = top_songs[top_songs['song_name'].notna()]
    
    if top_songs.empty:
        print("❌ No se encontraron canciones válidas.")
        return [{
            "artist_name": "Error",
            "song_name": "No se encontraron canciones",
            "spotify_url": "",
            "processed_lyrics": "No hay letra disponible",
            "translated_lyrics": "Traducción no disponible",
            "similarity": 0
        }]

    return top_songs[['artist_name', 'song_name', 'spotify_url', 'processed_lyrics', 'similarity']].to_dict(orient="records")
