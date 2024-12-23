from flask import request, jsonify
from server.models import db, Event
from . import event_blueprint
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


@event_blueprint.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    result = {
        event.event_id: {
            'name': event.name,
            'description': event.description,
            'location': event.location,
            'date': event.date.strftime('%Y-%m-%d')
        } for event in events
    }
    # result = [{
    #     'event_id': event.event_id,
    #     'name': event.name,
    #     'description': event.description,
    #     'location': event.location,
    #     'date': event.date.strftime('%Y-%m-%d')
    # } for event in events]
    return jsonify({"response": result}), 200


@event_blueprint.route('/', methods=['POST'])
def create_event():

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

    # Define the required fields
    required_fields = ['event_id', 'name', 'description', 'location', 'date']

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing_fields)}"
        }), 400

    # Check if event_id is a valid integer
    if not isinstance(data['event_id'], str) or not data['event_id'].startswith("eid_"):
        return jsonify({"error": "'event_id' should be an str, starts with eid_."}), 400

    # Check if data types are correct for other fields
    if not isinstance(data['name'], str) or not isinstance(data['description'], str) or not isinstance(data['location'], str):
        return jsonify({"error": "'name', 'description', and 'location' should be strings."}), 400
    if not isinstance(data['date'], str):
        return jsonify({"error": "'date' should be a string in 'YYYY-MM-DD' format."}), 400

    try:
        # Convert the date string to a Python date object
        event_date = datetime.strptime(data['date'], "%Y-%m-%d").date()

        # Check if event with the same event_id already exists
        existing_event = Event.query.filter_by(event_id=data['event_id']).first()
        if existing_event:
            return jsonify({"error": f"An event with the ID {data['event_id']} already exists."}), 400

        # Create a new event object
        new_event = Event(
            event_id=data['event_id'],
            name=data['name'],
            description=data['description'],
            location=data['location'],
            date=event_date
        )

        # Add to the database
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event created successfully"}), 201

    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Please use 'YYYY-MM-DD'."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500




# Update Event Endpoint
@event_blueprint.route('/<string:event_id>', methods=['PUT'])
def update_event(event_id):

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

    # Check if required fields are provided
    if not data or not all(field in data for field in ['name', 'location', 'date']):
        return jsonify({
            'error': 'Missing required fields. Please provide name, location, and date.'
        }), 400

    try:
        # Fetch event by ID or raise 404 if not found
        event = Event.query.get_or_404(event_id)

        # Update event details
        event.name = data['name']
        event.description = data.get('description', event.description)
        event.location = data['location']
        
        # Validate the date format
        try:
            event.date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
                'error': 'Invalid date format. Please use YYYY-MM-DD format.'
            }), 400

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Event updated successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error': f'Database error occurred: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'Event ID: {event_id} not found. Could not update your request.'
        }), 500


# Delete Event Endpoint
@event_blueprint.route('/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        # Fetch event by ID or raise 404 if not found
        event = Event.query.get_or_404(event_id)

        # Delete the event from the database
        db.session.delete(event)
        db.session.commit()

        return jsonify({'message': 'Event deleted successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error': f'Database error occurred: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'Event ID: {event_id} not found. Could not update your request.'
        }), 500
