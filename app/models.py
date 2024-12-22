from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Relationships with Attendee and Task models
    attendees = db.relationship('Attendee', backref='event', lazy=True)
    tasks = db.relationship('Task', backref='event', lazy=True)


class Attendee(db.Model):
    attendee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=True)

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    assigned_attendee_id = db.Column(db.Integer, db.ForeignKey('attendee.attendee_id'), nullable=True)
