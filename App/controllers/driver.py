from App.models import  driver,Inboxmessage
from App.database import db
from App.models.driver import Driver
from App.models.Drivelog import DriveLog
from App.models.resident import Resident
from App.models.Inboxmessage import Inboxmessage
from App.models.Request import Request
def schedule_drive(driver_id, city, licenseplate):
    # Ensure driver exists
    driver = Driver.query.get(driver_id)
    if not driver:
        return None  # driver not found
    
    # Create the new drive
    new_drivelog = DriveLog(city=city, licenseplate=licenseplate, driver_id=driver_id)
    db.session.add(new_drivelog)
    db.session.commit()
    
    # Notify all residents in the city
    residents = Resident.query.filter_by(city=city).all()
    for r in residents:
        new_inboxmessage = Inboxmessage(
            resident_id=r.id,
            drive_id=new_drivelog.id,
            message=f"New drive scheduled in {city} with License Plate: {licenseplate}"
        )
        db.session.add(new_inboxmessage)
    
    db.session.commit()  # commit all messages at once
    return new_drivelog

def change_request_status(request_id, new_status):
    request = Request.query.filter_by(id=request_id).first()
    if request:
        request.status = new_status
        db.session.commit()
        return request
    return None

def view_requests_driver(drive_id):
    requests = Request.query.filter_by(drive_id=drive_id).all()
    if requests:
        return requests 
    
    return None

def create_driver(username, password, fname, lname, phone):
    new_driver = Driver(username=username, password=password, fname=fname, lname=lname, phone=phone)
    db.session.add(new_driver)
    db.session.commit()
    return new_driver
