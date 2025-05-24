from flask import Blueprint,request, jsonify
from werkzeug.security import generate_password_hash
from models.user import User
from models.database import db
from utils.jwt_utils import generate_token
from utils.response_utils import success as success_response, error as error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Validación básica
        if not all(k in data for k in ['name', 'email', 'password', 'role']):
            return error_response("Faltan campos requeridos", 400)
        
        # Verifica si el usuario ya existe
        if User.query.filter_by(email=data['email']).first():
            return error_response("El email ya está registrado", 409)
        
        # Crea el usuario
        new_user = User(
            name=data['name'],
            email=data['email'],
            role=data['role']  # 'patient' o 'staff'
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        return success_response({"message": "Usuario registrado exitosamente"}, 201)
    
    except Exception as e:
        return error_response(str(e), 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return error_response("Credenciales inválidas", 401)
        
        token = generate_token(user.id, user.role)
        return success_response({"token": token, "role": user.role})
    
    except Exception as e:
        return error_response(str(e), 500)