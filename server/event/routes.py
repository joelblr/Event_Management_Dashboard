from flask import request, jsonify
from app.models import db, Event

@event_blueprint.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    result = [{
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'location': event.location,
        'date': event.date.strftime('%Y-%m-%d')
    } for event in events]
    return jsonify(result)

@event_blueprint.route('/', methods=['POST'])
def create_event():
    data = request.get_json()
    event = Event(
        name=data['name'],
        description=data.get('description'),
        location=data['location'],
        date=data['date']
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@event_blueprint.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get_or_404(event_id)
    event.name = data['name']
    event.description = data.get('description', event.description)
    event.location = data['location']
    event.date = data['date']
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@event_blueprint.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})
