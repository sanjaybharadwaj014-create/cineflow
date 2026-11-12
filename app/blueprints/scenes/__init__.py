from flask import Blueprint

scenes_bp = Blueprint('scenes', __name__, url_prefix='/scenes')

from app.blueprints.scenes import routes
