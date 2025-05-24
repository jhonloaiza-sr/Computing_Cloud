from flask import request,Blueprint
from models import Appointment, User, Availability
from models.database import db
from utils.jwt_utils import token_required, role_required
from utils.response_utils import success as success_response, error as error_response

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/appointments', methods=['GET'])
@token_required
@role_required('staff')
def get_all_appointments(current_user):
    try:
        status = request.args.get('status')  # Filtro opcional: ?status=confirmed
        query = Appointment.query
        if status:
            query = query.filter_by(status=status)
        
        appointments = query.join(User).join(Availability).all()
        
        return success_response([{
            "id": app.id,
            "patient": app.user.name,
            "date": app.availability.date.isoformat(),
            "time": str(app.availability.time),
            "status": app.status
        } for app in appointments])
    except Exception as e:
        return error_response(str(e), 500)

@staff_bp.route('/availability', methods=['POST'])
@token_required
@role_required('staff')
def add_availability(current_user):
    data = request.json
    try:
        new_slot = Availability(
            date=data['date'],  # Formato: 'YYYY-MM-DD'
            time=data['time'],  # Formato: 'HH:MM:SS'
            is_active=True
        )
        db.session.add(new_slot)
        db.session.commit()
        return success_response({"slot_id": new_slot.id}, 201)
    except Exception as e:
        return error_response(str(e), 500)