# Importa todos los modelos para que SQLAlchemy los detecte
from .database import db
from .user import User
from .availability import Availability
from .appointment import Appointment

__all__ = ['db', 'User', 'Availability', 'Appointment']
