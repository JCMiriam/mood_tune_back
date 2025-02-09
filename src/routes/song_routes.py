from flask import Blueprint, jsonify, request
from src.functions.song_search import search_songs

bp = Blueprint("song_routes", __name__, url_prefix="/songs")

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
