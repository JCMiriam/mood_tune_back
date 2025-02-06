import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config')

    # 🔹 Configuración de la sesión
    app.config['SESSION_TYPE'] = 'filesystem'  # Usa 'redis' si tienes Redis instalado
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), "flask_session")  # Carpeta donde se guardarán las sesiones
    app.config['SESSION_PERMANENT'] = False  # Las sesiones no deben ser permanentes
    app.config['SESSION_USE_SIGNER'] = True  # Firmar la sesión para mayor seguridad
    app.config['SESSION_COOKIE_NAME'] = 'moodtune_session'  # Nombre de la cookie de sesión
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protege la sesión de accesos por JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"  # Permite compartir cookies en localhost
    app.config['SESSION_COOKIE_SECURE'] = False  # ⚠️ False en localhost, True en producción
    app.config['SECRET_KEY'] = 'supersecretkey'  # Necesario para firmar sesiones y CSRF protection

    # Inicializar sesiones
    Session(app)

    # Configuración de CORS (permite credenciales)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Inicializar la base de datos
    db.init_app(app)
    Compress(app)

    # Registrar Blueprints (rutas)
    from src.routes import user_routes
    from src.functions.auth import auth_bp
    from src.routes.filtered_routes import filtered_bp

    app.register_blueprint(user_routes.bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(filtered_bp, url_prefix="/filter")

    return app
