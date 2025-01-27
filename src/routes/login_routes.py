from flask import Blueprint, redirect, request, jsonify
from src.functions.spotify_auth import (
    build_auth_url,
    exchange_code_for_token,
    refresh_access_token,
    is_code_used,
    mark_code_as_used,
)

login_bp = Blueprint("login", __name__)

# Spotify login redirect endpoint
@login_bp.route("/login")
def login():
    auth_url = build_auth_url()
    return redirect(auth_url)

# Callback endpoint
@login_bp.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400

    if is_code_used(code):
        return jsonify({"error": "Authorization code already used"}), 400

    mark_code_as_used(code)

    token_info = exchange_code_for_token(code)
    if "error" in token_info:
        return jsonify({"error": "Failed to fetch access token", "details": token_info}), 400

    return jsonify(token_info)

# Refresh access token endpoint
@login_bp.route("/refresh", methods=["POST"])
def refresh_token():
    refresh_token = request.json.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "No refresh token provided"}), 400

    new_tokens = refresh_access_token(refresh_token)
    if "error" in new_tokens:
        return jsonify({"error": "Failed to refresh token", "details": new_tokens}), 400

    return jsonify(new_tokens)