from flask import Blueprint, jsonify, request
from src.functions.song_search import search_songs
import pandas as pd

bp = Blueprint("song_routes", __name__, url_prefix="/songs")

# Función para calcular la tasa de diferencia entre las canciones de referencia
def calcular_tasa_diferencia_referencias(referencias, columnas_parametros):
    diferencias = []
    canciones_referencia = []
    promedio_diferencias = {}

    # Extraer la información de cada canción de referencia
    for referencia in referencias:
        cancion_data = referencia["dataset_data"]
        canciones_referencia.append(referencia)  # Guardamos la referencia completa
        promedio_diferencias[cancion_data["song_name"]] = 0

    # Comparar todas las canciones de referencia entre sí
    for i in range(len(canciones_referencia)):
        for j in range(i + 1, len(canciones_referencia)):
            song_1 = canciones_referencia[i]["dataset_data"]
            song_2 = canciones_referencia[j]["dataset_data"]
            diferencia_total = 0

            for columna in columnas_parametros:
                valor_1 = song_1[columna] * 10
                valor_2 = song_2[columna] * 10
                diferencia_total += (abs(valor_1 - valor_2)) ** 2

            diferencias.append({
                "song_1": song_1["song_name"],
                "artist_1": song_1["artist_name"],
                "song_2": song_2["song_name"],
                "artist_2": song_2["artist_name"],
                "tasa_diferencia": diferencia_total
            })

            # Acumular diferencias para el promedio
            promedio_diferencias[song_1["song_name"]] += diferencia_total
            promedio_diferencias[song_2["song_name"]] += diferencia_total

    # Calcular el promedio de diferencia para cada canción
    for cancion in promedio_diferencias:
        promedio_diferencias[cancion] /= (len(canciones_referencia) - 1)

    # Convertir a DataFrame y ordenar
    diferencias_df = pd.DataFrame(diferencias)
    diferencias_df.sort_values(by="tasa_diferencia", ascending=True, inplace=True)

    # Crear DataFrame con promedios y ordenarlo
    promedio_df = pd.DataFrame(list(promedio_diferencias.items()), columns=["song_name", "promedio_diferencia"])
    promedio_df.sort_values(by="promedio_diferencia", ascending=True, inplace=True)

    # Obtener la lista ordenada de canciones con su estructura completa
    canciones_ordenadas = []
    for _, row in promedio_df.iterrows():
        song_name = row["song_name"]
        cancion_completa = next(ref for ref in canciones_referencia if ref["dataset_data"]["song_name"] == song_name)
        canciones_ordenadas.append(cancion_completa)

    return diferencias_df, canciones_ordenadas

# Endpoint para obtener canción basada en el estado de ánimo
@bp.route("/mood", methods=["POST"])
def get_songs_by_mood():
    """
    Endpoint para buscar canciones basadas en el estado de ánimo del usuario.
    Recibe un JSON con la clave `moodText`.
    """
    data = request.get_json()
    if not data or "moodText" not in data:
        return jsonify({"error": "Falta el parámetro 'moodText'"}), 400

    mood_text = data["moodText"]
    songs = search_songs(mood_text, top_n=15)

    return jsonify(songs)

# Endpoint para obtener canción más cercana a las demás
@bp.route("/rank-central-songs", methods=["POST"])
def rank_central_songs():
    try:
        data = request.get_json()

        if not data or "references" not in data or "importances" not in data:
            return jsonify({"error": "Invalid input format"}), 400

        referencias = data["references"]
        importancias = data["importances"]

        if not referencias or not isinstance(importancias, dict):
            return jsonify({"error": "Invalid references or importances format"}), 400

        # Obtener columnas de parámetros a partir del diccionario de importancias
        columnas_parametros = list(importancias.keys())

        # Calcular la centralidad de las canciones
        _, canciones_ordenadas = calcular_tasa_diferencia_referencias(referencias, columnas_parametros)

        return jsonify({"ordered_tracks": canciones_ordenadas}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500