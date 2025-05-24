from models import Appointment, Availability, User
from models.database import db
from datetime import datetime
from utils.response_utils import error

class AppointmentService:
    @staticmethod
    def get_available_slots():
        """Obtiene todos los horarios disponibles"""
        return Availability.query.filter_by(is_active=True).all()

    @staticmethod
    def book_appointment(user_id, availability_id, notes=None):
        """Reserva una cita médica"""
        slot = Availability.query.get(availability_id)
        
        if not slot or not slot.is_active:
            return error("Horario no disponible", 400)
        
        if Appointment.query.filter_by(availability_id=availability_id).first():
            return error("El horario ya está reservado", 400)

        try:
            new_appointment = Appointment(
                user_id=user_id,
                availability_id=availability_id,
                notes=notes,
                status='pending'
            )
            db.session.add(new_appointment)
            db.session.commit()
            return new_appointment
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def cancel_appointment(appointment_id, user_id=None, reason=None):
        """Cancela una cita (para paciente o staff)"""
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return error("Cita no encontrada", 404)
        
        if user_id and appointment.user_id != user_id:
            return error("No autorizado", 403)

        try:
            appointment.status = 'cancelled'
            appointment.cancellation_reason = reason
            db.session.commit()
            return appointment
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_patient_appointments(user_id):
        """Obtiene todas las citas de un paciente"""