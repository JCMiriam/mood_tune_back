import os
import requests

# Load env variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPES = "playlist-read-private playlist-read-collaborative user-library-read user-top-read"

used_codes = set()

def build_auth_url():
    """
    Build the Spotify authentication URL.
    """
    return (
        f"{SPOTIFY_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={SCOPES.replace(' ', '%20')}"
        f"&redirect_uri={REDIRECT_URI}"
    )

def exchange_code_for_token(code):
    """
    Exchange an authorization code for an access token.
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
    Refresh the access token using the refresh token.
    """
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    return response.json()

def is_code_used(code):
    """
    Verify if an autorization code has been used.
    """
    return code in used_codes

def mark_code_as_used(code):
    """
    Set an autorization code as used.
    """
    used_codes.add(code)
