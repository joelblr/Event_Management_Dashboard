from flask import request, jsonify
from app.models import db, Attendee
from . import attendee_blueprint
from sqlalchemy.exc import SQLAlchemyError



# Route to get all attendees
@attendee_blueprint.route('/', methods=['GET'])
def get_all_attendees():
    try:
        attendees = Attendee.query.all()
        if not attendees:
            return jsonify({"message": "No attendees found."}), 404
        attendees_data = [{"attendee_id": attendee.attendee_id, "name": attendee.name, "email": attendee.email, "event_id": attendee.event_id} for attendee in attendees]
        return jsonify({"attendees": attendees_data}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Route to add a new attendee
@attendee_blueprint.route('/', methods=['POST'])
def add_attendee():

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': 'The request body must be a valid JSON object.'
        }), 500

    # Check if the data is not a dictionary (invalid JSON format or unexpected structure)
    if not isinstance(data, dict):
        return jsonify({
            'error': 'The request body must be a valid JSON object.'
        }), 400

    # Check if the data is empty
    if not data:
        return jsonify({
            'error': 'The request body cannot be empty. Please provide valid data.'
        }), 400

    # Check for missing fields
    required_fields = ['name', 'email', 'event_id']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Validate event_id
    try:
        event = Event.query.get(data['event_id'])
        if not event:
            return jsonify({"error": "Event not found with the provided event_id."}), 404
    except Exception as e:
        return jsonify({"error": f"Invalid event_id. Error: {str(e)}"}), 400

    # Validate email format
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format."}), 400

    try:
        # Create and add the new attendee
        new_attendee = Attendee(name=data['name'], email=data['email'], event_id=data['event_id'])
        db.session.add(new_attendee)
        db.session.commit()
        return jsonify({"message": "Attendee added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Route to update an attendee's information
@attendee_blueprint.route('/<int:attendee_id>', methods=['PUT'])
def update_attendee(attendee_id):

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': 'The request body must be a valid JSON object.'
        }), 500

    # Check if the data is not a dictionary (invalid JSON format or unexpected structure)
    if not isinstance(data, dict):
        return jsonify({
            'error': 'The request body must be a valid JSON object.'
        }), 400

    # Check if the data is empty
    if not data:
        return jsonify({
            'error': 'The request body cannot be empty. Please provide valid data.'
        }), 400
    
    # Check if attendee exists
    attendee = Attendee.query.get(attendee_id)
    if not attendee:
        return jsonify({"error": f"Attendee with id {attendee_id} not found."}), 404

    # Check for missing or incorrect fields
    if 'name' in data:
        attendee.name = data['name']
    if 'email' in data:
        if '@' not in data['email']:
            return jsonify({"error": "Invalid email format."}), 400
        attendee.email = data['email']
    if 'event_id' in data:
        event = Event.query.get(data['event_id'])
        if not event:
            return jsonify({"error": "Event not found with the provided event_id."}), 404
        attendee.event_id = data['event_id']
    
    try:
        db.session.commit()
        return jsonify({"message": "Attendee updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Route to remove an attendee
@attendee_blueprint.route('/<int:attendee_id>', methods=['DELETE'])
def remove_attendee(attendee_id):
    attendee = Attendee.query.get(attendee_id)
    if not attendee:
        return jsonify({"error": f"Attendee with id {attendee_id} not found."}), 404

    try:
        db.session.delete(attendee)
        db.session.commit()
        return jsonify({"message": "Attendee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500