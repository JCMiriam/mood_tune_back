from flask import Blueprint, jsonify, request
from flask_cors import CORS
from src.functions.dataset_loader import check_songs_in_dataset, check_artists_in_dataset


filtered_bp = Blueprint("filtered", __name__, url_prefix="/filter")
CORS(filtered_bp, resources={r"/*": {"origins": "http://localhost:5173"}})

@filtered_bp.route("/filtered-top-tracks", methods=["OPTIONS", "POST"])
def filtered_top_tracks():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_tracks = data.get("tracks", [])
    filtered_tracks = check_songs_in_dataset(user_tracks)
    return jsonify({"filtered_tracks": filtered_tracks})

@filtered_bp.route("/filtered-followed-artists", methods=["OPTIONS", "POST"])
def filtered_followed_artists():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_artists = data.get("artists", [])
    filtered_artists = check_artists_in_dataset(user_artists)
    return jsonify({"filtered_artists": filtered_artists})

@filtered_bp.route("/filtered-favourite-tracks", methods=["OPTIONS", "POST"])
def filtered_favourite_tracks():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_tracks = data.get("tracks", [])
    filtered_tracks = check_songs_in_dataset(user_tracks)
    return jsonify({"filtered_tracks": filtered_tracks})
