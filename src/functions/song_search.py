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
    detected_lang = detect(text)
    if detected_lang != 'en':
        return GoogleTranslator(source='auto', target='en').translate(text)
    return text

def translate_to_spanish(text):
    """Traduce una letra de inglés a español."""
    return GoogleTranslator(source='en', target='es').translate(text) if isinstance(text, str) else "Traducción no disponible"

def search_songs(user_query, top_n=5):
    """
    Busca canciones en base a una frase del usuario usando FAISS.
    
    - user_query: Texto ingresado por el usuario.
    - top_n: Número de canciones recomendadas.
    """
    start_time = time.time()
    
    translated_query = translate_to_english(user_query)
    query_embedding = model.encode(translated_query, convert_to_tensor=True).cpu().numpy().astype('float32')

    distances, indices = index.search(np.array([query_embedding]), top_n)
    
    top_songs = df.iloc[indices[0]].copy()
    top_songs['similarity'] = 1 - distances[0]  

    # 📌 Traducir letras
    top_songs['translated_lyrics'] = top_songs['processed_lyrics'].apply(lambda x: translate_to_spanish(x[:500]) if isinstance(x, str) else "Traducción no disponible")

    print(f"⏱ Búsqueda completada en {time.time() - start_time:.4f} segundos.")

    return top_songs[['artist_name', 'song_name', 'spotify_url', 'processed_lyrics', 'translated_lyrics', 'similarity']]
