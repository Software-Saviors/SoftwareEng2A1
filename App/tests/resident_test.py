import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
from App.models import resident
from App.controllers import (
    create_resident,
    create_request,
    view_inbox,
    view_requests_resident
)

LOGGER = logging.getLogger(__name__)

'''Unit Tests'''

class ResidentUnitTests(unittest.TestCase):
    def test_new_resident(self):
        new_resident = resident("testresident", "testpassword", "Test", "Resident", "7654321")
        assert new_resident is not None
        assert new_resident.id is not None
        assert new_resident.username == "testresident"
        assert new_resident.fname == "Test"
        assert new_resident.lname == "Resident"
        assert new_resident.phonenumber == "7654321"

'''Integration Tests'''

class ResidentIntegrationTests(unittest.TestCase):
    def test_create_resident(self):
        resident = create_resident(
            username="testresident",
            password="testpassword",
            fname="Test",
            lname="Resident",
            phone="7654321"
        )
        assert resident is not None
        assert resident.id is not None
        assert resident.username == "testresident"
        assert resident.fname == "Test"
        assert resident.lname == "Resident"
        assert resident.phonenumber == "7654321"

    def test_create_request(self):
        resident = create_resident(
            username="testresident",
            password="testpassword",
            fname="Test",
            lname="Resident",
            phone="7654321"
        )

        request= create_request(
            resident_id=resident.id,
            drive_id=1,
            address="123 Test St"
        )
        
        assert request is not None
        assert request.id is not None
        assert request.resident_id == resident.id
        assert request.drive_id == 1
        assert request.address == "123 Test St"

    def test_view_inbox(self):
        resident = create_resident(
            username="testresident",
            password="testpassword",
            fname="Test",
            lname="Resident",
            phone="7654321"
        )

        inbox= view_inbox(resident.id)
        assert inbox == []

    def test_view_requests_resident(self):
        resident = create_resident(
            username="testresident",
            password="testpassword",
            fname="Test",
            lname="Resident",
            phone="7654321"
        )

        requests = view_requests_resident(resident.id)
        assert requests == []