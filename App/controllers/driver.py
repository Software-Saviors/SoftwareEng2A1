from App.models import  driver,Inboxmessage, Request
from App.database import db
from App.models.driver import Driver
from App.models.Drivelog import DriveLog
from App.models.resident import Resident
from App.models.Inboxmessage import Inboxmessage
def schedule_drive(driver_id,city, liscenseplate):
    if driver:
        new_drivelog = DriveLog(city=city, liscenseplate=liscenseplate, driver_id=driver_id)
        Residents = Resident.query.filter_by(city=city).all()
    
    
    for r in Residents:
        new_inboxmessage = Inboxmessage(
            message=f"New drive scheduled in {city} with License Plate: {liscenseplate}",
            drive_id=new_drivelog.id,
            resident_id=Resident.id, 
        )
        db.session.add(new_inboxmessage)
        db.session.add(new_drivelog)
        db.session.commit()
        return new_drivelog

def change_request_status(request_id, new_status):
    request = Request.query.filter_by(id=request_id).first()
    if request:
        request.status = new_status
        db.session.commit()
        return request
    return None

def view_requests(drive_id):
    requests = Request.query.filter_by(drive_id=drive_id).all()
    if requests:
        return requests 
    
    return None

def create_driver(username, password, fname, lname, phone):
    new_driver = Driver(username=username, password=password, fname=fname, lname=lname, phone=phone)
    db.session.add(new_driver)
    db.session.commit()
    return new_driver
