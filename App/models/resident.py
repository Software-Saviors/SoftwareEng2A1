from App.database import db
from .user import User

class Resident(User):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(100), nullable=False)
   
    requested_drives = db.relationship('DriveRequest', backref='resident', lazy=True)
    requested_drives = db.relationship('DriveRequest', back_populates='tenant')

    
    def __init__(self,fname,lname, phonenumber, email, address, City):
        self.fname = fname
        self.lname = lname
        self.phonenumber = phonenumber
        self.email = email
        self.address = address
        self.City = City 