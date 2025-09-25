from App.database import db
from datetime import datetime
from .resident import Resident

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('DriveLog.id'), nullable=True)
    request_time = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, accepted, rejected, completed

    resident = db.relationship('Resident', backref='requests')

def __init__(self, resident_id):
    self.resident_id = resident_id
    self.status = 'pending'