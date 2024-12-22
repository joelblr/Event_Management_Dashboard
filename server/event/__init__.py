from flask import Blueprint

event_blueprint = Blueprint('event', __name__)

from . import routes
