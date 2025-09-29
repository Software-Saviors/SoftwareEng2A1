import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.models.driver import Driver
from App.controllers.driver import create_driver, schedule_drive, view_requests, change_request_status
from App.controllers.resident import create_resident, create_request, view_inbox

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("usertype", default="resident")
def create_user_command(username, password, usertype):
    create_user(username, password, usertype)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)



driver_cli = AppGroup('driver', help='Driver object commands')

@driver_cli.command("create", help="Creates a driver")
@click.argument("username", default="driver1")
@click.argument("password", default="driverpass")
@click.argument("fname", default="Driver")
@click.argument("lname", default="One")
@click.argument("phone", default="1234567890")
def create_driver_command(username, password, fname, lname, phone):
    
    create_driver(username, password, fname, lname, phone)
    print(f'Driver {fname} {lname} created!')

app.cli.add_command(driver_cli) # add the group to the cli

@driver_cli.command("schedule_drive", help="Schedule a drive and notify residents")
@click.argument("driver_id", type=int, default=1)
@click.argument("City", default="Chaguanas")
@click.argument("LiscensePlate", default="ABC123")
def schedule_drive_command(driver_id, City, LiscensePlate):
    drivelog = schedule_drive(driver_id, City, LiscensePlate)
    if drivelog:
        print(f'Drive scheduled in {City} with License Plate: {LiscensePlate}')
    else:
        print('Driver not found or no residents in the specified city.')
app.cli.add_command(driver_cli) # add the group to the cli

@driver_cli.command("view_requests", help="View requests for a specific drive")
@click.argument("drive_id", type=int, default=1)
def view_requests_command(drive_id):
    requests = view_requests(drive_id)
    if requests:
        for req in requests:
            print(f'Request ID: {req.id}, Status: {req.status}, Resident ID: {req.resident_id}, Address: {req.address}, Request Time: {req.request_time}')
    else:
        print('No requests found for this drive or invalid drive ID.')
app.cli.add_command(driver_cli) # add the group to the cli

@driver_cli.command("change_request_status", help="Change the status of a request")
@click.argument("request_id", type=int, default=1)
@click.argument("new_status", default="pending")
def change_request_status_command(request_id, new_status):
    request = change_request_status(request_id, new_status)
    if request:
        print(f'Request ID: {request.id} status changed to {request.status}')
    else:
        print('Request not found.')



resident_cli = AppGroup('resident', help='Resident object commands')

@resident_cli.command("create", help="Creates a resident")
@click.argument("username", default="resident1")    
@click.argument("password", default="residentpass")
@click.argument("fname", default="Resident")
@click.argument("lname", default="One")
@click.argument("phonenumber", default="0987654321")
@click.argument("City", default="Chaguanas")
@click.argument("address", default="123 Main St")
def create_resident_command(username, password, fname, lname, phonenumber, City, address):
    
    create_resident( username, password, fname, lname, phonenumber, City, address)
    print(f'Resident {fname} {lname} created!')
app.cli.add_command(resident_cli) # add the group to the cli

@resident_cli.command("create_request", help="Create a service request")
@click.argument("resident_id", type=int, default=1)
@click.argument("drive_id", type=int, default=None)
@click.argument("address", default="456 Another St")
def create_request_command(resident_id, drive_id, address):
  
    new_request = create_request(resident_id, drive_id, address)
    print(f'Request ID: {new_request.id} created for Resident ID: {resident_id} to Address: {address}')
app.cli.add_command(resident_cli) # add the group to the cli

@resident_cli.command("view_inbox", help="View inbox messages for a resident")
@click.argument("resident_id", type=int, default=1)
def view_inbox_command(resident_id):
 
    messages = view_inbox(resident_id)
    if messages:
        for msg in messages:
            print(f'Message ID: {msg.id}, From Driver ID: {msg.driver_id}, Message: {msg.Message}, Time: {msg.timestamp}')
    else:
        print('No messages found or invalid resident ID.')
app.cli.add_command(resident_cli) # add the group to the cli



