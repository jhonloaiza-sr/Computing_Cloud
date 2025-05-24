from flask import Blueprint

# Creación de Blueprints
auth_bp = Blueprint('auth', __name__)
patient_bp = Blueprint('patient', __name__)
staff_bp = Blueprint('staff', __name__)

# Importa las rutas al final para evitar circular imports
from .auth import auth_bp
from .patient import patient_bp
from .staff import staff_bp
from .errors import register_error_handlers
#from . import auth, patient, staff, errors
