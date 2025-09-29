from App.models import resident,Request,Inboxmessage
from App.database import db


def create_request(resident_id, drive_id, address):
    new_request = Request(
        resident_id=resident_id,
        drive_id=drive_id,
        status='Pending',
        address=address
    )
    db.session.add(new_request)
    db.session.commit()
    return new_request

def view_inbox(resident_id):
    Inboxmessages = Inboxmessage.query.filter_by(resident_id=resident_id).all()
    return Inboxmessages


def create_resident(username, password, fname, lname, phonenumber, city, address):
    new_resident = resident(username=username, password=password, fname=fname, lname=lname, phonenumber=phonenumber, city=city, address=address)
    db.session.add(new_resident)
    db.session.commit()
    return new_resident