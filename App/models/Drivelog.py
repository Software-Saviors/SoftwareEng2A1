from App.database import db
from datetime import datetime, timezone


class DriveLog(db.Model):
    __tablename__ = 'drive_log'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    city = db.Column(db.String(50))
    licenseplate = db.Column(db.String(20))
    
    driver = db.relationship('Driver', back_populates='drive_logs')
    requests = db.relationship('Request', back_populates='drive')
    
    def __init__(self, driver_id, city, licenseplate):
      self.driver_id = driver_id
      self.city = city
      self.licenseplate = licenseplate
    


