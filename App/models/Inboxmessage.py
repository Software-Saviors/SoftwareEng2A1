from App.database import db
from datetime import datetime, timezone
timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Inboxmessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident = db.Column(db.Integer, db.ForeignKey('residents.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive_log.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=timestamp)
    resident_rel = db.relationship('Resident', back_populates='inbox_messages')
    
    def __init__(self, message,drive_id):
        self.message = message
        self.drive_id = drive_id
        self.timestamp = datetime.now(datetime.timezone.utc)