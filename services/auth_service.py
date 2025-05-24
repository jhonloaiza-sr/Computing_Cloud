from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.database import db
from utils.jwt_utils import generate_token
from utils.response_utils import error

class AuthService:
    @staticmethod
    def register_user(name, email, password, role):
        """Registra un nuevo usuario en la base de datos"""
        if User.query.filter_by(email=email).first():
            return error("El email ya está registrado", 409)
        
        try:
            new_user = User(
                name=name,
                email=email,
                role=role
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def login_user(email, password):
        """Autentica un usuario y genera JWT"""
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None
        
        return {
            "token": generate_token(user.id, user.role),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }