import os
import requests
from flask import Blueprint, request, redirect, jsonify
from urllib.parse import urlencode

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://mood-tune-front.onrender.com")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1/me"

SCOPES = "playlist-read-private playlist-read-collaborative user-library-read user-top-read"

def build_auth_url():
    query_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    return f"{SPOTIFY_AUTH_URL}?{urlencode(query_params)}"

def exchange_code_for_token(code):
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    return response.json()

def refresh_access_token(refresh_token):
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    return response.json()

@auth_bp.route("/login")
def login():
    return redirect(build_auth_url())

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    token_response = exchange_code_for_token(code)

    if "access_token" not in token_response:
        return jsonify({"error": "Failed to get access token", "details": token_response}), 400

    redirect_url = f"{FRONTEND_URL}/callback?access_token={token_response['access_token']}&refresh_token={token_response['refresh_token']}&expires_in={token_response['expires_in']}"
    return redirect(redirect_url)

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.json
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Refresh token missing"}), 400

    new_token_data = refresh_access_token(refresh_token)

    if "access_token" not in new_token_data:
        return jsonify({"error": "Failed to refresh token", "details": new_token_data}), 400

    return jsonify(new_token_data)

@auth_bp.route("/me")
def get_user_profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Access token required"}), 401

    access_token = auth_header.replace("Bearer ", "").strip()

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_API_URL, headers=headers)

    if response.status_code == 401:
        refresh_token = request.headers.get("Refresh-Token")
        if not refresh_token:
            return jsonify({"error": "Invalid access token, refresh token required"}), 401

        new_token_data = refresh_access_token(refresh_token)
        if "access_token" in new_token_data:
            new_access_token = new_token_data["access_token"]

            headers["Authorization"] = f"Bearer {new_access_token}"
            retry_response = requests.get(SPOTIFY_API_URL, headers=headers)

            if retry_response.status_code == 200:
                return jsonify(retry_response.json())

        return jsonify({"error": "Invalid access token, refresh failed"}), 401

    return jsonify(response.json())

@auth_bp.route("/playlists")
def get_user_playlists():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"error": "Access token required"}), 401

    headers = {"Authorization": access_token}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    return jsonify(response.json())

@auth_bp.route("/top-tracks")
def get_top_tracks():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"error": "Access token required"}), 401

    headers = {"Authorization": access_token}
    response = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=50", headers=headers)

    return jsonify(response.json())

@auth_bp.route("/top-artists")
def get_top_artists():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"error": "Access token required"}), 401

    headers = {"Authorization": access_token}
    response = requests.get("https://api.spotify.com/v1/me/top/artists?limit=50", headers=headers)

    return jsonify(response.json())

@auth_bp.route("/favorite-tracks")
def get_favorite_tracks():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"error": "Access token required"}), 401

    headers = {"Authorization": access_token}
    response = requests.get("https://api.spotify.com/v1/me/tracks?limit=50", headers=headers)

    return jsonify(response.json())
