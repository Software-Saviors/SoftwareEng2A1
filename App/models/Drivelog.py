from App.database import db
from datetime import datetime
from .driver import Driver

class DriveLog(db.Model):
    __tablename__ = 'drive_log'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    City = db.Column(db.String(50))
    LiscensePlate = db.Column(db.String(20))
    
    driver = db.relationship('Driver', backref='drive_logs')
    
def __init__(self, driver_id, City, LiscensePlate):
    self.driver_id = driver_id
    self.City = City
    self.LiscensePlate = LiscensePlate
    