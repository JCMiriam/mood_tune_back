import os
import requests
from flask import Blueprint, request, redirect, jsonify
from urllib.parse import urlencode

# Configurar Blueprint de autenticación
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Cargar variables de entorno
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# URLs de Spotify
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1/me"

SCOPES = "playlist-read-private playlist-read-collaborative user-library-read user-top-read"

def build_auth_url():
    """
    Construye la URL de autenticación de Spotify.
    """
    query_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    return f"{SPOTIFY_AUTH_URL}?{urlencode(query_params)}"

def exchange_code_for_token(code):
    """
    Intercambia un código de autorización por un token de acceso.
    """
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
    """
    Refresca un token de acceso usando el token de actualización.
    """
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
    """
    Redirige al usuario a la autenticación de Spotify.
    """
    return redirect(build_auth_url())

@auth_bp.route("/callback")
def callback():
    """
    Maneja la respuesta de autenticación de Spotify.
    """
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    token_response = exchange_code_for_token(code)

    if "access_token" not in token_response:
        return jsonify({"error": "Failed to get access token", "details": token_response}), 400

    return jsonify(token_response)

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Recibe un refresh token y devuelve un nuevo access token.
    """
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
    """
    Obtiene información del usuario autenticado.
    """
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"error": "Access token required"}), 401

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_API_URL, headers=headers)

    return jsonify(response.json())
