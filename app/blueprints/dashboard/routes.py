from datetime import date
from flask import render_template
from app.blueprints.dashboard import dashboard_bp
from app.models import (
    Film, Scene, CastCrew, ShootingSchedule,
    PRODUCTION_STATUS_CHOICES
)

@dashboard_bp.route('/')
def index():
    today_str = date.today().isoformat()

    # Core statistics requested
    total_films = Film.query.count()
    total_scenes = Scene.query.count()
    completed_scenes = Scene.query.filter_by(status='Completed').count()

    # Upcoming shooting schedules (future or today with active/scheduled status)
    upcoming_schedules = ShootingSchedule.query.filter(
        ShootingSchedule.date >= today_str,
        ShootingSchedule.status.in_(['Scheduled', 'In Progress'])
    ).order_by(ShootingSchedule.date.asc(), ShootingSchedule.call_time.asc()).limit(6).all()

    # Today's shoot if any
    today_schedules = ShootingSchedule.query.filter_by(date=today_str).all()

    # Current production status breakdown
    status_counts = {
        status: Film.query.filter_by(production_status=status).count()
        for status in PRODUCTION_STATUS_CHOICES
    }

    # Scene status breakdown
    scene_status_counts = {
        'Draft': Scene.query.filter_by(status='Draft').count(),
        'Scheduled': Scene.query.filter_by(status='Scheduled').count(),
        'Shooting': Scene.query.filter_by(status='Shooting').count(),
        'Completed': Scene.query.filter_by(status='Completed').count(),
    }

    # Active films for quick overview table
    active_films = Film.query.order_by(Film.id.desc()).all()

    # Overall progress percentage
    scene_progress_pct = round((completed_scenes / total_scenes * 100)) if total_scenes > 0 else 0
    total_crew = CastCrew.query.count()

    return render_template(
        'dashboard/index.html',
        total_films=total_films,
        total_scenes=total_scenes,
        completed_scenes=completed_scenes,
        scene_progress_pct=scene_progress_pct,
        upcoming_schedules=upcoming_schedules,
        today_schedules=today_schedules,
        status_counts=status_counts,
        scene_status_counts=scene_status_counts,
        active_films=active_films,
        total_crew=total_crew,
        production_statuses=PRODUCTION_STATUS_CHOICES,
        today_str=today_str
    )
