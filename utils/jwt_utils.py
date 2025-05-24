import jwt
from datetime import datetime, timedelta
from flask import request
from config import Config
from functools import wraps
from utils.response_utils import error as error_response

def generate_token(user_id, role):
    """Genera un token JWT válido por 24 horas"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verifica y decodifica un token JWT"""
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

def token_required(f):
    """Decorador para endpoints que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return error_response(401, "Token requerido")
        try:
            current_user = verify_token(token.split()[1])
        except Exception as e:
            return error_response(403, str(e))
        return f(current_user, *args, **kwargs)
    return decorated

def role_required(required_role):
    """Decorador para validación de roles"""
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.get('role') != required_role:
                return error_response(403, "Acceso no autorizado para este rol")
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator