import numpy as np
import time
from deep_translator import GoogleTranslator
from langdetect import detect
from src.models.model_loader import model_data

# 📌 Importar los datos pre-cargados
df = model_data["df"]
index = model_data["index"]
model = model_data["model"]

def translate_to_english(text):
    """Traduce la frase del usuario a inglés si no está en inglés."""
    try:
        if text and isinstance(text, str) and text.strip():
            detected_lang = detect(text)
            if detected_lang != 'en':
                return GoogleTranslator(source='auto', target='en').translate(text)
        return text
    except Exception as e:
        print(f"❌ Error detectando idioma: {e}")
        return text  # Si hay error, usa el texto original

def translate_to_spanish(text):
    """Traduce una letra de inglés a español (máx 499 caracteres)."""
    try:
        if text and isinstance(text, str) and text.strip():  # Asegura que no sea vacío o None
            return GoogleTranslator(source='en', target='es').translate(text[:499])
        return "Traducción no disponible"
    except Exception as e:
        print(f"❌ Error traduciendo letra: {e}")
        return "Traducción no disponible"

def search_songs(user_query, top_n=15):
    """
    Busca canciones en base a una frase del usuario usando FAISS.
    
    - user_query: Texto ingresado por el usuario.
    - top_n: Número de canciones recomendadas.
    """
    start_time = time.time()
    
    # 📌 Traducir la consulta a inglés si es necesario
    translated_query = translate_to_english(user_query)

    # 📌 Convertir la consulta en embedding
    query_embedding = model.encode(translated_query, convert_to_tensor=True).cpu().numpy().astype('float32')

    # 📌 Buscar en FAISS
    distances, indices = index.search(np.array([query_embedding]), top_n)

    # 📌 Verificar si se obtuvieron resultados válidos
    if not indices.any():
        print("❌ No se encontraron resultados, devolviendo valor por defecto.")
        return [{
            "artist_name": "Error",
            "song_name": "No se encontraron canciones",
            "spotify_url": "",
            "processed_lyrics": "No hay letra disponible",
            "translated_lyrics": "Traducción no disponible",
            "similarity": 0
        }]

    # 📌 Obtener las canciones más similares
    top_songs = df.iloc[indices[0]].copy()
    top_songs['similarity'] = 1 - distances[0]  # Convertir distancia en similitud

    # 📌 Filtrar canciones inválidas
    top_songs = top_songs[top_songs['song_name'].notna()]
    if top_songs.empty:
        print("❌ La búsqueda no devolvió canciones válidas.")
        return [{
            "artist_name": "Error",
            "song_name": "No se encontraron canciones",
            "spotify_url": "",
            "processed_lyrics": "No hay letra disponible",
            "translated_lyrics": "Traducción no disponible",
            "similarity": 0
        }]

    # 📌 Asegurar que `processed_lyrics` existe antes de traducir y cortar a 499 caracteres
    if "processed_lyrics" in top_songs.columns:
        top_songs['processed_lyrics'] = top_songs['processed_lyrics'].apply(
            lambda x: (x[:499] + "...") if isinstance(x, str) and x.strip() else "Letra no disponible"
        )
        top_songs['translated_lyrics'] = top_songs['processed_lyrics'].apply(
            lambda x: translate_to_spanish(x) if x != "Letra no disponible" else "Traducción no disponible"
        )
    else:
        top_songs['processed_lyrics'] = "Letra no disponible"
        top_songs['translated_lyrics'] = "Traducción no disponible"

    print(f"⏱ Búsqueda completada en {time.time() - start_time:.4f} segundos.")

    # 📌 Retornar datos estructurados para la UI
    return top_songs[['artist_name', 'song_name', 'spotify_url', 'processed_lyrics', 'translated_lyrics', 'similarity']].to_dict(orient="records")
