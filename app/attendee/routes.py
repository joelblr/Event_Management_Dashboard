from flask import request, jsonify
from app.models import db, Attendee, Task
from . import attendee_blueprint
from sqlalchemy.exc import SQLAlchemyError


import re

def validate_email(email):
    """
    Validates an email address based on the following rules:
    1. The domain must be "caafrwsb.com".
    2. The local part (username) must:
        - Start with a letter.
        - Contain only alphanumeric characters, periods, underscores, and hyphens.
        - Be between 6 and 64 characters.
    3. The email must not exceed 45 characters.
    4. Prevent injection attacks by checking for unusual characters.

    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if len(email) > 74 or len(email) < 16:
        return False

    # Define the regex for the email format
    pattern = re.compile(r"""
        ^([a-zA-Z][a-zA-Z0-9._-]{5,64})   # Local part: starts with a letter, allows certain characters
        @                                  # @ symbol
        (gmail\.com)$                 # Domain must be "caafrwsb.com"
    """, re.VERBOSE)

    # Check if the email matches the regex
    if not pattern.match(email):
        return False

    # Additional security checks: Prevent injections or unsafe characters
    if any(char in email for char in ['\n', '\r', '\t', '\0', '\x0b', '\x0c']):
        return False
    return True


@attendee_blueprint.route('/', methods=['GET'])
def get_all_attendees():
    try:
        attendees = Attendee.query.all()
        
        if not attendees:
            return jsonify({"error": "No attendees found. Add Attendees to view them."}), 404
        
        attendee_list = [{"name": attendee.name, "email": attendee.email} for attendee in attendees]
        return jsonify({"attendees": attendee_list}), 200
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# API to add a new attendee
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
    required_fields = ['name', 'email']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    if not validate_email(data['email']):
        return jsonify({"error": f"Invalid email: {data['email']}"}), 400

    try:
        # Check if attendee already exists
        if Attendee.query.get(data['email']):
            return jsonify({"error": "An attendee with this email already exists"}), 400

        # Create and save attendee
        new_attendee = Attendee(name=data['name'], email=data['email'])
        db.session.add(new_attendee)
        db.session.commit()

        return jsonify({"message": "Attendee created successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# API to update an existing attendee
@attendee_blueprint.route('/<string:attendee_email>', methods=['PUT'])
def update_attendee(attendee_email):
    try:
        # Parse the JSON request body
        data = request.get_json()
    except Exception:
        return jsonify({
            'error': 'The request body must be a valid JSON object.'
        }), 400

    # Ensure the data is a dictionary and not empty
    if not isinstance(data, dict) or not data:
        return jsonify({
            'error': 'The request body must be a non-empty JSON object.'
        }), 400

    # Fetch the attendee by email
    attendee = Attendee.query.get(attendee_email)
    if not attendee:
        return jsonify({"error": "Attendee not found"}), 404

    try:
        # Update the attendee's fields if provided
        new_name = data.get('name')
        new_email = data.get('email')

        # Update the name if provided
        if new_name:
            attendee.name = new_name

        if not validate_email(new_email):
            return jsonify({"error": f"Invalid email: {new_email}"}), 400

        # Update the email if provided and ensure it's unique
        if new_email and new_email != attendee.email:
            email_in_use = Attendee.query.filter_by(email=new_email).first()
            if email_in_use:
                return jsonify({"error": "The provided email is already in use by another attendee."}), 409
            attendee.email = new_email

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Attendee updated successfully"}), 200

    except ValueError:
        return jsonify({"error": "Invalid data type provided. Ensure all fields have the correct data types."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@attendee_blueprint.route('/<string:attendee_email>', methods=['DELETE'])
def delete_attendee(attendee_email):
    # Check if the attendee exists
    attendee = Attendee.query.filter_by(email=attendee_email).first()
    if not attendee:
        return jsonify({'error': 'Attendee not found'}), 404
    
    # Check if the attendee is assigned to any tasks
    tasks = Task.query.filter_by(assigned_attendee_email=attendee.email).all()
    if tasks:
        return jsonify({'error': 'Attendee cannot be deleted because they are assigned to tasks.'}), 400

    # Proceed with deletion
    db.session.delete(attendee)
    db.session.commit()
    return jsonify({'message': 'Attendee deleted successfully'}), 200
