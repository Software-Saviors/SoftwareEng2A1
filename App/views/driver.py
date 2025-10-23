from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from App.controllers import (
    create_driver,
    schedule_drive,
    view_requests_driver,
    change_request_status
)

driver_views = Blueprint('driver_views', __name__)

@driver_views.route('/api/drivers', methods=['POST'])
def create_driver_action():
    """Create a new driver (admin only)"""
    data = request.json
    
    # Basic authorization check - you might want to add admin role check
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    fname = data.get('fname')
    lname = data.get('lname')
    phone = data.get('phone')
    
    if not all([username, password, fname, lname, phone]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        new_driver = create_driver(username, password, fname, lname, phone)
        return jsonify({
            'message': f'Driver {fname} {lname} created successfully',
            'driver': {
                'id': new_driver.id,
                'username': new_driver.username,
                'fname': new_driver.fname,
                'lname': new_driver.lname,
                'phone': new_driver.phone
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@driver_views.route('/api/drives', methods=['POST'])
@jwt_required()
def schedule_drive_action():
    """Schedule a new drive (driver only)"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Get the current user's ID from JWT
    driver_id = int(get_jwt_identity())
    city = data.get('city')
    license_plate = data.get('license_plate')
    
    if not all([city, license_plate]):
        return jsonify({'error': 'Missing required fields: city, license_plate'}), 400
    
    try:
        drivelog = schedule_drive(driver_id, city, license_plate)
        if drivelog:
            return jsonify({
                'message': f'Drive scheduled in {city} with License Plate: {license_plate}',
                'drive': {
                    'id': drivelog.id,
                    'city': drivelog.city,
                    'license_plate': drivelog.liscenseplate,
                    'driver_id': drivelog.driver_id
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to schedule drive'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@driver_views.route('/api/drives/<int:drive_id>/requests', methods=['GET'])
@jwt_required()
def view_drive_requests(drive_id):
    """View all requests for a specific drive (driver only)"""
    try:
        # Optional: Add authorization to check if current user is the driver for this drive
        requests = view_requests_driver(drive_id)
        
        if requests:
            requests_data = [{
                'id': req.id,
                'status': req.status,
                'resident_id': req.resident_id,
                'address': req.address,
                'timestamp': req.timestamp.strftime("%Y-%d-%m %I:%M %p") if req.timestamp else None
            } for req in requests]
            
            return jsonify({
                'drive_id': drive_id,
                'requests': requests_data
            }), 200
        else:
            return jsonify({
                'drive_id': drive_id,
                'requests': [],
                'message': 'No requests found for this drive'
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@driver_views.route('/api/requests/<int:request_id>/status', methods=['PATCH'])
@jwt_required()
def update_request_status(request_id):
    """Change the status of a request (driver only)"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    # Validate status values
    valid_statuses = ['pending', 'accepted', 'rejected', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({
            'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400
    
    try:
        updated_request = change_request_status(request_id, new_status)
        
        if updated_request:
            return jsonify({
                'message': f'Request status updated to {new_status}',
                'request': {
                    'id': updated_request.id,
                    'status': updated_request.status,
                    'resident_id': updated_request.resident_id,
                    'address': updated_request.address,
                    'timestamp': updated_request.timestamp.strftime("%Y-%d-%m %I:%M %p") if updated_request.timestamp else None
                }
            }), 200
        else:
            return jsonify({'error': 'Request not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500