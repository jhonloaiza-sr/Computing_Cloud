from .database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'), nullable=False)
    availability = db.relationship('Availability', backref='appointments')
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled', name='appointment_status'), 
                      default='pending')
    notes = db.Column(db.Text)
    cancellation_reason = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'
