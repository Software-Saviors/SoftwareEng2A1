from App.database import db
from .user import User
class Driver(User):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    drive_logs = db.relationship('DriveLog', back_populates='driver')

    def __init__(self,fname, lname, phone,):
        self.fname = fname
        self.lname = lname
        self.phone = phone
        