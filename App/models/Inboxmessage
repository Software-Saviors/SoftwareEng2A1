from App.database import db
from datetime import datetime
from .resident import Resident

class Inboxmessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    drive = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))

    resident_rel = db.relationship('Resident', backref='inboxmessages')

    def __init__(self, message):
        self.message = message
        self.timestamp = datetime.now(datetime.timezone.utc)