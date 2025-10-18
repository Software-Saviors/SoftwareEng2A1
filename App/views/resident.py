from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from App.controllers import (
    create_resident,
    create_request,
    view_inbox,
    view_requests_resident
)

resident_views = Blueprint('resident_views', __name__)

@resident_views.route('/api/residents', methods=['POST'])
def create_resident_action():
    """Create a new resident (public registration)"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    fname = data.get('fname')
    lname = data.get('lname')
    phonenumber = data.get('phonenumber')
    city = data.get('city')
    address = data.get('address')
    
    if not all([username, password, fname, lname, phonenumber, city, address]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        new_resident = create_resident(username, password, fname, lname, phonenumber, city, address)
        return jsonify({
            'message': f'Resident {fname} {lname} created successfully',
            'resident': {
                'id': new_resident.id,
                'username': new_resident.username,
                'fname': new_resident.fname,
                'lname': new_resident.lname,
                'phonenumber': new_resident.phonenumber,
                'city': new_resident.city,
                'address': new_resident.address
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resident_views.route('/api/requests', methods=['POST'])
@jwt_required()
def create_request_action():
    """Create a service request (resident only)"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Get the current user's ID from JWT
    resident_id = int(get_jwt_identity())
    drive_id = data.get('drive_id')
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Missing required field: address'}), 400
    
    try:
        new_request = create_request(resident_id, drive_id, address)
        return jsonify({
            'message': f'Request created successfully',
            'request': {
                'id': new_request.id,
                'resident_id': new_request.resident_id,
                'drive_id': new_request.drive_id,
                'address': new_request.address,
                'status': new_request.status,
                'timestamp': new_request.timestamp.isoformat() if new_request.timestamp else None
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resident_views.route('/api/residents/<int:resident_id>/inbox', methods=['GET'])
@jwt_required()
def view_resident_inbox(resident_id):
    """View inbox messages for a resident (resident only - own inbox)"""
    # Authorization: users can only view their own inbox
    current_user_id = int(get_jwt_identity())
    
    if current_user_id != resident_id:
        return jsonify({'error': 'Unauthorized - You can only view your own inbox'}), 403
    
    try:
        messages = view_inbox(resident_id)
        
        if messages:
            messages_data = [{
                'id': msg.id,
                'drive_id': msg.drive_id,
                'message': msg.message,
                'timestamp': msg.timestamp.isoformat() if msg.timestamp else None
            } for msg in messages]
            
            return jsonify({
                'resident_id': resident_id,
                'messages': messages_data
            }), 200
        else:
            return jsonify({
                'resident_id': resident_id,
                'messages': [],
                'message': 'No messages found'
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@resident_views.route('/api/residents/<int:resident_id>/requests', methods=['GET'])
@jwt_required()
def view_resident_requests(resident_id):
    """View service requests for a resident (resident only - own requests)"""
    # Authorization: users can only view their own requests
    current_user_id = int(get_jwt_identity())
    
    if current_user_id != resident_id:
        return jsonify({'error': 'Unauthorized - You can only view your own requests'}), 403
    
    try:
        requests = view_requests_resident(resident_id)
        
        if requests:
            requests_data = [{
                'id': req.id,
                'status': req.status,
                'drive_id': req.drive_id,
                'address': req.address,
                'timestamp': req.timestamp.isoformat() if req.timestamp else None
            } for req in requests]
            
            return jsonify({
                'resident_id': resident_id,
                'requests': requests_data
            }), 200
        else:
            return jsonify({
                'resident_id': resident_id,
                'requests': [],
                'message': 'No requests found'
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500