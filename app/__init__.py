from flask import Flask
from app.event import event_blueprint
# from flask_sqlalchemy import SQLAlchemy
from app.models import db
from app.attendee import attendee_blueprint
# from app.task import task_blueprint
# from app.auth import auth_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(event_blueprint, url_prefix='/events')
    app.register_blueprint(attendee_blueprint, url_prefix='/attendees')
    # app.register_blueprint(task_blueprint, url_prefix='/tasks')
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
