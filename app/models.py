from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Event Model
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    # Relationships with Attendee and Task models
    tasks = db.relationship('Task', backref='event', lazy=True)

# Attendee Model (no reference to Event anymore)
class Attendee(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationship with Task model
    tasks = db.relationship('Task', backref='attendee', lazy=True)

# Task Model (foreign keys to Attendee and Event)
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    assigned_attendee_email = db.Column(db.Integer, db.ForeignKey('attendee.email'), nullable=True)
