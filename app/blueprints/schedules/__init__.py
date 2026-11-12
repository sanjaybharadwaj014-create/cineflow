from flask import Blueprint

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

from app.blueprints.schedules import routes
