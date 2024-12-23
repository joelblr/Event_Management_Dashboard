from flask import Blueprint

task_blueprint = Blueprint('task', __name__)

from . import routes
