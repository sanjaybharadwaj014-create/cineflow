import os
from flask import Flask
from app.config import Config
from app.models import db
from app.seed_data import seed_sample_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.films import films_bp
    from app.blueprints.scenes import scenes_bp
    from app.blueprints.crew import crew_bp
    from app.blueprints.schedules import schedules_bp
    from app.blueprints.production import production_bp
    from app.blueprints.api import api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(films_bp)
    app.register_blueprint(scenes_bp)
    app.register_blueprint(crew_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(production_bp)
    app.register_blueprint(api_bp)

    # Context processors for global template helpers
    @app.context_processor
    def inject_helpers():
        def status_badge_class(status):
            mapping = {
                'Pre-production': 'badge-purple',
                'Shooting': 'badge-amber',
                'Post-production': 'badge-cyan',
                'Completed': 'badge-emerald',
                'Draft': 'badge-secondary',
                'Scheduled': 'badge-blue',
                'In Progress': 'badge-amber',
                'Postponed': 'badge-orange',
                'Cancelled': 'badge-danger'
            }
            return mapping.get(status, 'badge-secondary')

        def day_night_icon(day_night):
            if 'NIGHT' in day_night:
                return '🌙'
            elif 'DAWN' in day_night or 'DUSK' in day_night:
                return '🌅'
            return '☀️'

        return dict(
            status_badge_class=status_badge_class,
            day_night_icon=day_night_icon
        )

    # Setup database and seed data inside application context
    with app.app_context():
        db.create_all()
        # Seed sample data if database is fresh
        seed_sample_data()

    return app
