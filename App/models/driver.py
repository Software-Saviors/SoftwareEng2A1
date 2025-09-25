from App.database import db
from .user import User

class Driver(User):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, email, password, fname, lname, phone,):
        self.set_password(password)
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email