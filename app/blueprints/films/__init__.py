from flask import Blueprint

films_bp = Blueprint('films', __name__, url_prefix='/films')

from app.blueprints.films import routes
