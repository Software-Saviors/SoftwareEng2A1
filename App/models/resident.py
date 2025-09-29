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
    
    inbox_messages = db.relationship('Inboxmessage', back_populates='resident_rel')
    requested_drives = db.relationship('Request', back_populates='resident')

    def __init__(self, username,fname, lname, phonenumber, address, city,password):
        super().__init__(username, password, user_type='resident')
        self.fname = fname
        self.lname = lname
        self.phonenumber = phonenumber
        self.address = address
        self.city = city