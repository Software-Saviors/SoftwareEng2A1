from .user import create_user
from App.database import db
from App.controllers.resident import create_resident
from App.controllers.driver import create_driver
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_resident( 'steve', 'steve123', 'Steven', 'Deonarine', '6798984' ,'Chaguanas', 'Savannah_Rd')
    create_driver( 'rob', 'robpass', 'Robert', 'Francis', '87654321')