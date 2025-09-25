from App.models import Resident, Driver,Inboxmessage,Drivelog
from App.database import db

def schedule_drive(driver_id,City, LiscensePlate):
    driver = Driver.query.get(driver_id)
    if driver:
        new_drivelog = Drivelog(City=City, LiscensePlate=LiscensePlate, driver_id=driver_id)
        residents = Resident.query.filter_by(city=City).all()
    
    
    for resident in residents:
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