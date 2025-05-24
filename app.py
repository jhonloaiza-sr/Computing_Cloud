# app.py - Punto de entrada principal de la aplicación
from flask import Flask, jsonify,render_template
from flask_cors import CORS
from models.database import init_db, db
from routes import (
    auth_bp, 
    patient_bp, 
    staff_bp,
    register_error_handlers
)
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    # Configuración inicial de Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    # Habilitar CORS (útil para desarrollo)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "https://tudominio.com"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })

    # Configuración de logging
    def configure_logging(app):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/clinic_app.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        
    configure_logging(app)

    # Inicializar base de datos
    init_db(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(staff_bp)

    # Registrar manejadores de errores
    register_error_handlers(app)

    # Ruta de prueba
    @app.route('/')
    def home():
        app.logger.info("Inicio visitado")
        return jsonify({"msg": "Backend funcionando!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
       
