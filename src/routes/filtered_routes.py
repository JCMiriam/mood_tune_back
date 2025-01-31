from flask import Blueprint, jsonify, request
from src.functions.dataset_loader import check_songs_in_dataset, check_artists_in_dataset

# Crear un Blueprint para estas rutas
filtered_bp = Blueprint("filtered", __name__)

@filtered_bp.route("/filtered-top-tracks", methods=["POST"])
def filtered_top_tracks():
    user_tracks = request.json.get("tracks", [])
    filtered_tracks = check_songs_in_dataset(user_tracks)
    return jsonify({"filtered_tracks": filtered_tracks})

@filtered_bp.route("/filtered-followed-artists", methods=["POST"])
def filtered_followed_artists():
    user_artists = request.json.get("artists", [])
    filtered_artists = check_artists_in_dataset(user_artists)
    return jsonify({"filtered_artists": filtered_artists})

@filtered_bp.route("/filtered-favourite-tracks", methods=["POST"])
def filtered_favourite_tracks():
    user_tracks = request.json.get("tracks", [])
    filtered_tracks = check_songs_in_dataset(user_tracks)
    return jsonify({"filtered_tracks": filtered_tracks})
