from flask import jsonify, request
from app.blueprints.api import api_bp
from app.models import Film, Scene, ShootingSchedule, CastCrew, PRODUCTION_STATUS_CHOICES

@api_bp.route('/stats')
def stats():
    total_films = Film.query.count()
    total_scenes = Scene.query.count()
    completed_scenes = Scene.query.filter_by(status='Completed').count()

    status_counts = {
        s: Film.query.filter_by(production_status=s).count()
        for s in PRODUCTION_STATUS_CHOICES
    }

    scene_status_counts = {
        'Draft': Scene.query.filter_by(status='Draft').count(),
        'Scheduled': Scene.query.filter_by(status='Scheduled').count(),
        'Shooting': Scene.query.filter_by(status='Shooting').count(),
        'Completed': Scene.query.filter_by(status='Completed').count(),
    }

    return jsonify({
        'total_films': total_films,
        'total_scenes': total_scenes,
        'completed_scenes': completed_scenes,
        'film_status_counts': status_counts,
        'scene_status_counts': scene_status_counts
    })

@api_bp.route('/films/<int:film_id>/scenes')
def film_scenes(film_id):
    scenes = Scene.query.filter_by(film_id=film_id).all()
    return jsonify([s.to_dict() for s in scenes])
