from App.models import resident, driver,Inboxmessage,Drivelog, Request
from App.database import db

def schedule_drive(driver_id,City, LiscensePlate):
    current_driver = driver.query.get(driver_id)
    if driver:
        new_drivelog = Drivelog(City=City, LiscensePlate=LiscensePlate, driver_id=driver_id)
        residents = resident.query.filter_by(city=City).all()
    
    
    for r in residents:
        new_inboxmessage = Inboxmessage(
            Message=f"New drive scheduled in {City} with License Plate: {LiscensePlate}",
            driver_id=driver_id,
            resident_id=resident.id, 
            drive_id=new_drivelog.id  
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
    new_driver = driver(username=username, password = password, fname=fname, lname=lname, phone=phone)
    db.session.add(new_driver)
    db.session.commit()
    return new_driver
  