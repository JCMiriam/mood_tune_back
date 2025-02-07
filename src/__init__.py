from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_cors import CORS

# SQLAlchemy Instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config')

    # Initialize extensions
    db.init_app(app)
    Compress(app)
    CORS(app)

    # Register routes
    from src.routes import user_routes
    from src.functions.auth import auth_bp
    from src.routes.filtered_routes import filtered_bp
    from src.routes.song_routes import bp as song_routes_bp 
    

    app.register_blueprint(user_routes.bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(filtered_bp, url_prefix="/filter")
    app.register_blueprint(song_routes_bp, url_prefix="/songs")


    return app
