from App.models.Request import Request
import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
from App.models import driver
from App.controllers import (
    schedule_drive,
    change_request_status,
    view_requests_driver,
    create_driver
)


LOGGER = logging.getLogger(__name__)

'''Unit Testing'''

class DriverUnitTests(unittest.TestCase):
    def test_new_driver(self):
        new_driver = driver("testdriver", "testpassword", "Test", "Driver", "1234567")
        assert driver.id is not None
        assert driver.username == "testdriver"
        assert driver.fname == "Test"
        assert driver.lname == "Driver"
        assert driver.phone == "1234567"

'''Integration Testing'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class DriverIntegrationTests(unittest.TestCase):

    def test_create_driver(self):
        driver = create_driver(
            username="testdriver",
            password="testpassword",
            fname="Test",
            lname="Driver",
            phone="1234567"
        )
        assert driver is not None
        assert driver.id is not None
        assert driver.username == "testdriver"
        assert driver.fname == "Test"
        assert driver.lname == "Driver"
        assert driver.phone == "1234567"

    def test_schedule_drive(self):
        driver = create_driver(
            username="testdriver",
            password="testpassword",
            fname="Test",
            lname="Driver",
            phone="1234567"
        )
        assert driver is not None
        assert driver.id is not None
        assert driver.username == "testdriver"
        assert driver.fname == "Test"
        assert driver.lname == "Driver"
        assert driver.phone == "1234567"

        driverlog = schedule_drive(
            driver_id=driver.id,
            city="TestCity",
            licenseplate="TST1234"
        )

        assert driverlog is not None
        assert driverlog.driver_id == driver.id
        assert driverlog.city == "TestCity"
        assert driverlog.licenseplate == "TST1234"

    def test_change_request_status(self):
        driver = create_driver(
            username="testdriver",
            password="testpassword",
            fname="Test",
            lname="Driver",
            phone="1234567"
        )

        driverlog = schedule_drive(
            driver_id=driver.id,
            city="TestCity",
            licenseplate="TST1234"
        )
        
        request = Request(
            resident_id=1,
            drive_id=driverlog.id,
            address="123 Test St"
        )

        request = change_request_status(request.id, 'accepted')
        assert request.status == 'accepted'

    def test_view_requests_driver(self):
        driver = create_driver(
            username="testdriver",
            password="testpassword",
            fname="Test",
            lname="Driver",
            phone="1234567"
        )

        driverlog = schedule_drive(
            driver_id=driver.id,
            city="TestCity",
            licenseplate="TST1234"
        )

        request = Request(
            resident_id=1,
            drive_id=driverlog.id,
            address="123 Test St"
        )

        requests = view_requests_driver(driver.id)
        assert len(requests) == 1
        assert requests[0].id == request.id
        assert requests[0].resident_id == 1
        assert requests[0].driver_id == driverlog.id
        assert requests[0].status == 'pending'
        assert requests[0].address == "123 Test St"