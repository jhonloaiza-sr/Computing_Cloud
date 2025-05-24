from .database import db

class Availability(db.Model):
    __tablename__ = 'availability'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    # Relaciones
    appointments = db.relationship('Appointment', backref='availability', lazy=True)

    def __repr__(self):
        return f'<Availability {self.date} {self.time}>'
