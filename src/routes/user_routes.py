from flask import Blueprint, request, jsonify
#from src.functions.user_service import save_user_and_tracks

bp = Blueprint('user_routes', __name__, url_prefix='/user')

#@bp.route('/save', methods=['POST'])
#def save_user_data():
#    data = request.json
#    user_data = data['user']
#    tracks_data = data['tracks']

#    try:
#        save_user_and_tracks(user_data, tracks_data)
#        return jsonify({'message': 'Saved data'}), 200
#    except Exception as e:
#        return jsonify({'error': str(e)}), 500

@bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to MoodTune"}), 200

