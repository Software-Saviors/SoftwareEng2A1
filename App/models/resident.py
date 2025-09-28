from App.database import db
from .user import User

class Resident(User):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    

    requested_drives = db.relationship('DriveRequest', back_populates='resident')

    def __init__(self, fname, lname, phonenumber, address, city,password):
        self.fname = fname
        self.lname = lname
        self.phonenumber = phonenumber
        self.address = address
        self.city = city