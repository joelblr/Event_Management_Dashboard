from flask import Flask
from server.event import event_blueprint
# from flask_sqlalchemy import SQLAlchemy
from server.models import db
from server.attendee import attendee_blueprint
from server.task import task_blueprint
# from server.auth import auth_blueprint

def create_server():
    server = Flask(__name__)
    server.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(server)

    # Register blueprints
    server.register_blueprint(event_blueprint, url_prefix='/events')
    server.register_blueprint(attendee_blueprint, url_prefix='/attendees')
    server.register_blueprint(task_blueprint, url_prefix='/tasks')
    # server.register_blueprint(auth_blueprint, url_prefix='/auth')

    return server
