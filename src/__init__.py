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
    app.register_blueprint(user_routes.bp, url_prefix="/users")

    return app
