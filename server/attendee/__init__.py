from flask import Blueprint

attendee_blueprint = Blueprint('attendee', __name__)

from . import routes
