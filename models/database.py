from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app: Flask):
    """Inicializa la conexión a la base de datos con tus credenciales RDS"""
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mysql+mysqlconnector://admin:Elzancudo980407@consultorio-medico-db.cqjmquca03y1.us-east-1.rds.amazonaws.com/consultorio_db"
    )
    
    # Configuraciones adicionales para optimización
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita warnings
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # Recicla conexiones cada 1h
    
    # Inicializa la base de datos
    db.init_app(app)
    
    # Verifica la conexión (opcional, para debug)
    with app.app_context():
        try:
            db.engine.connect()
            print("✅ Conexión a RDS MySQL exitosa!")
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos: {str(e)}")