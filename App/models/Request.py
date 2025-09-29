from App.database import db
from datetime import datetime, timezone


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive_log.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, accepted, rejected, completed
    address = db.Column(db.String(200), nullable=False)
    resident = db.relationship('Resident', back_populates='requested_drives')

def __init__(self, resident_id, address):
    self.resident_id = resident_id
    self.status = 'pending'
    self.address = address