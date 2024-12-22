@task_blueprint.route('/', methods=['POST'])
def create_task():
    data = request.get_json()

    # Check for missing fields
    required_fields = ['name', 'deadline', 'event_id', 'assigned_attendee_email']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        # Validate event
        event = Event.query.get(data['event_id'])
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Validate attendee
        attendee = Attendee.query.get(data['assigned_attendee_email'])
        if not attendee:
            return jsonify({"error": "Attendee not found"}), 404

        # Parse deadline
        deadline = datetime.strptime(data['deadline'], "%Y-%m-%d").date()

        # Create and save task
        new_task = Task(
            name=data['name'],
            deadline=deadline,
            event_id=data['event_id'],
            assigned_attendee_email=data['assigned_attendee_email']
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Task created successfully"}), 201

    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
