from flask import render_template, request, redirect, url_for, flash
from app.blueprints.production import production_bp
from app.models import (
    db, Film, Scene, CastCrew, ShootingSchedule,
    PRODUCTION_STATUS_CHOICES
)

@production_bp.route('/')
def index():
    # Group films by production status
    stages = {status: [] for status in PRODUCTION_STATUS_CHOICES}
    films = Film.query.order_by(Film.id.desc()).all()

    for film in films:
        if film.production_status in stages:
            stages[film.production_status].append(film)
        else:
            stages['Pre-production'].append(film)

    # Calculate overall metrics
    total_films = len(films)
    total_scenes = Scene.query.count()
    completed_scenes = Scene.query.filter_by(status='Completed').count()
    active_shoots = ShootingSchedule.query.filter_by(status='In Progress').count()

    overall_progress = round((completed_scenes / total_scenes * 100)) if total_scenes > 0 else 0

    return render_template(
        'production/index.html',
        stages=stages,
        production_statuses=PRODUCTION_STATUS_CHOICES,
        total_films=total_films,
        total_scenes=total_scenes,
        completed_scenes=completed_scenes,
        active_shoots=active_shoots,
        overall_progress=overall_progress
    )

@production_bp.route('/update-stage/<int:film_id>', methods=['POST'])
def update_stage(film_id):
    film = db.get_or_404(Film, film_id)
    new_status = request.form.get('production_status')

    if new_status in PRODUCTION_STATUS_CHOICES:
        old_status = film.production_status
        film.production_status = new_status
        db.session.commit()
        flash(f'Film "{film.title}" moved from {old_status} → {new_status}.', 'success')
    else:
        flash('Invalid production status specified.', 'danger')

    return redirect(request.referrer or url_for('production.index'))
