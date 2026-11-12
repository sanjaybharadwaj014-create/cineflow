from flask import Blueprint

crew_bp = Blueprint('crew', __name__, url_prefix='/crew')

from app.blueprints.crew import routes
