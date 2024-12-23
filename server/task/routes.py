from flask import Flask, request, jsonify
from server.models import db, Task, Event, Attendee  # assuming models are already defined
from . import task_blueprint
from datetime import datetime


@task_blueprint.route('', methods=['POST'])
def create_task():
    data = request.get_json()

    # Validate required fields
    if not data.get('name') or not data.get('deadline') or not data.get('event_id'):
        return jsonify({
            'status': 'failure',
            'message': 'Missing required fields: name, deadline, event_id.'
        }), 400

    # Convert the deadline string to a date object
    try:
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'status': 'failure',
            'message': 'Invalid date format for deadline. Expected format: YYYY-MM-DD.'
        }), 400

    # Check if event exists
    event = Event.query.get(data['event_id'])
    if not event:
        return jsonify({
            'status': 'failure',
            'message': f"Event with ID {data['event_id']} not found."
        }), 404

    # Check if attendee exists (optional)
    if data.get('assigned_attendee_email'):
        attendee = Attendee.query.get(data['assigned_attendee_email'])
        if not attendee:
            return jsonify({
                'status': 'failure',
                'message': f"Attendee with email {data['assigned_attendee_email']} not found."
            }), 404

    # Create and add the task
    task = Task(
        task_id=data.get('task_id', None),  # optional if task_id is auto-generated
        name=data['name'],
        deadline=deadline,  # Use the parsed date object
        status=data.get('status', 'Pending'),
        event_id=data['event_id'],
        assigned_attendee_email=data.get('assigned_attendee_email')
    )
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Task created successfully.',
            'task_id': task.task_id,
            'name': task.name,
            'deadline': task.deadline,
            'status': task.status,
            'event_id': task.event_id,
            'assigned_attendee_email': task.assigned_attendee_email
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'failure',
            'message': f"Error creating task: {str(e)}"
        }), 500

# Endpoint to get a task by ID
@task_blueprint.route('/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            'status': 'success',
            'task_id': task.task_id,
            'name': task.name,
            'deadline': task.deadline,
            'status': task.status,
            'event_id': task.event_id,
            'assigned_attendee_email': task.assigned_attendee_email
        }), 200
    else:
        return jsonify({
            'status': 'failure',
            'message': f"Task with ID {task_id} not found."
        }), 404

# Endpoint to get all tasks for an event
@task_blueprint.route('/events/<string:event_id>', methods=['GET'])
def get_tasks_for_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({
            'status': 'failure',
            'message': f"Event with ID {event_id} not found."
        }), 404

    tasks = Task.query.filter_by(event_id=event_id).all()
    return jsonify({
        'status': 'success',
        'tasks': [
            {
                'task_id': task.task_id,
                'name': task.name,
                'deadline': task.deadline,
                'status': task.status,
                'event_id': task.event_id,
                'assigned_attendee_email': task.assigned_attendee_email
            } for task in tasks
        ]
    }), 200

# Endpoint to update a task
@task_blueprint.route('/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)

    if task:
        task.name = data.get('name', task.name)
        task.deadline = data.get('deadline', task.deadline)
        task.status = data.get('status', task.status)
        task.assigned_attendee_email = data.get('assigned_attendee_email', task.assigned_attendee_email)

        try:
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Task updated successfully.',
                'task_id': task.task_id,
                'name': task.name,
                'deadline': task.deadline,
                'status': task.status,
                'event_id': task.event_id,
                'assigned_attendee_email': task.assigned_attendee_email
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'failure',
                'message': f"Error updating task: {str(e)}"
            }), 500
    else:
        return jsonify({
            'status': 'failure',
            'message': f"Task with ID {task_id} not found."
        }), 404

# Endpoint to delete a task
@task_blueprint.route('/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task:
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f"Task with ID {task_id} deleted successfully."
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'failure',
                'message': f"Error deleting task: {str(e)}"
            }), 500
    else:
        return jsonify({
            'status': 'failure',
            'message': f"Task with ID {task_id} not found."
        }), 404


# app = Flask(__name__)

# # Endpoint to create a new task
# @app.route('/', methods=['POST'])
# def create_task():
#     data = request.get_json()
#     try:
#         event = Event.query.get(data['event_id'])  # Check if the event exists
#         if not event:
#             return jsonify({'message': 'Event not found'}), 404
        
#         task = Task(
#             name=data['name'],
#             deadline=data['deadline'],
#             status=data['status'],
#             event_id=data['event_id'],
#             assigned_attendee_id=data.get('assigned_attendee_id')  # Optional
#         )
#         db.session.add(task)
#         db.session.commit()
#         return jsonify({'message': 'Task created', 'task': task.to_dict()}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': str(e)}), 400

# # Endpoint to get a task by its ID
# @app.route('/<string:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = Task.query.get(task_id)
#     if task:
#         return jsonify({'task': task.to_dict()}), 200
#     else:
#         return jsonify({'message': 'Task not found'}), 404

# # Endpoint to get all tasks for a specific event
# @app.route('/api/events/<string:event_id>/tasks', methods=['GET'])
# def get_tasks_for_event(event_id):
#     event = Event.query.get(event_id)
#     if not event:
#         return jsonify({'message': 'Event not found'}), 404

#     tasks = Task.query.filter_by(event_id=event_id).all()
#     return jsonify({'tasks': [task.to_dict() for task in tasks]}), 200

# # Endpoint to update a task
# @app.route('/api/tasks/<string:task_id>', methods=['PUT'])
# def update_task(task_id):
#     data = request.get_json()
#     task = Task.query.get(task_id)

#     if task:
#         task.name = data.get('name', task.name)
#         task.deadline = data.get('deadline', task.deadline)
#         task.status = data.get('status', task.status)
#         task.assigned_attendee_id = data.get('assigned_attendee_id', task.assigned_attendee_id)

#         db.session.commit()
#         return jsonify({'message': 'Task updated', 'task': task.to_dict()}), 200
#     else:
#         return jsonify({'message': 'Task not found'}), 404

# # Endpoint to delete a task
# @app.route('/api/tasks/<string:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     task = Task.query.get(task_id)
#     if task:
#         db.session.delete(task)
#         db.session.commit()
#         return jsonify({'message': 'Task deleted'}), 200
#     else:
#         return jsonify({'message': 'Task not found'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
