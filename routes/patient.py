from flask import request,Blueprint
from models import Appointment, Availability
from models.database import db
from utils.jwt_utils import token_required, role_required
from utils.response_utils import success as success_response, error as error_response
from services.appointment_service import AppointmentService
from services.email_service import EmailService
from models.user import User

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/availability', methods=['GET'])
@token_required
@role_required('patient')
def get_availability(current_user):
    try:
        slots = Availability.query.filter_by(is_active=True).all()
        return success_response([{
            "id": slot.id,
            "date": slot.date.isoformat(),
            "time": str(slot.time)
        } for slot in slots])
    except Exception as e:
        return error_response(str(e), 500)

@patient_bp.route('/appointments', methods=['POST'])
@token_required
@role_required('patient')
def book_appointment(current_user):
    data = request.json
    try:
        slot = Availability.query.get(data['availability_id'])
        if not slot or not slot.is_active:
            return error_response("Horario no disponible", 400)
        
        new_appointment = Appointment(
            user_id=current_user.id,
            availability_id=slot.id,
            status='pending'
        )
        db.session.add(new_appointment)
        db.session.commit()
        
        return success_response({"appointment_id": new_appointment.id}, 201)
    except Exception as e:
        return error_response(str(e), 500)