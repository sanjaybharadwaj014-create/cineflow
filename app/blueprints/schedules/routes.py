from datetime import date
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.schedules import schedules_bp
from app.models import (
    db, ShootingSchedule, Scene, Film,
    SCHEDULE_STATUS_CHOICES
)

@schedules_bp.route('/')
def index():
    view_filter = request.args.get('view', 'all').strip()  # all, upcoming, today, completed
    film_id = request.args.get('film_id', type=int)
    search_query = request.args.get('q', '').strip()
    today_str = date.today().isoformat()

    query = ShootingSchedule.query

    if film_id:
        query = query.filter_by(film_id=film_id)

    if view_filter == 'upcoming':
        query = query.filter(ShootingSchedule.date >= today_str, ShootingSchedule.status != 'Completed')
    elif view_filter == 'today':
        query = query.filter_by(date=today_str)
    elif view_filter == 'completed':
        query = query.filter_by(status='Completed')

    if search_query:
        query = query.filter(
            (ShootingSchedule.location.ilike(f'%{search_query}%')) |
            (ShootingSchedule.call_time.ilike(f'%{search_query}%')) |
            (ShootingSchedule.notes.ilike(f'%{search_query}%'))
        )

    schedules = query.order_by(ShootingSchedule.date.asc(), ShootingSchedule.call_time.asc()).all()
    films = Film.query.order_by(Film.title.asc()).all()

    return render_template(
        'schedules/index.html',
        schedules=schedules,
        films=films,
        selected_film_id=film_id,
        current_view=view_filter,
        search_query=search_query,
        today_str=today_str,
        schedule_statuses=SCHEDULE_STATUS_CHOICES
    )

@schedules_bp.route('/create', methods=['GET', 'POST'])
def create():
    films = Film.query.order_by(Film.title.asc()).all()
    scenes = Scene.query.order_by(Scene.film_id.asc(), Scene.scene_number.asc()).all()
    today_str = date.today().isoformat()

    if request.method == 'POST':
        scene_id = request.form.get('scene_id', type=int)
        shoot_date = request.form.get('date', '').strip()
        location = request.form.get('location', '').strip()
        call_time = request.form.get('call_time', '').strip()
        status = request.form.get('status', 'Scheduled').strip()
        notes = request.form.get('notes', '').strip()

        if not scene_id or not shoot_date or not location or not call_time:
            flash('Please specify Scene, Date, Location, and Call time.', 'danger')
            return render_template(
                'schedules/form.html',
                action='create',
                schedule=None,
                films=films,
                scenes=scenes,
                today_str=today_str,
                schedule_statuses=SCHEDULE_STATUS_CHOICES
            )

        scene = db.session.get(Scene, scene_id)
        if not scene:
            flash('Selected scene does not exist.', 'danger')
            return redirect(url_for('schedules.create'))

        schedule = ShootingSchedule(
            film_id=scene.film_id,
            scene_id=scene.id,
            date=shoot_date,
            location=location,
            call_time=call_time,
            status=status if status in SCHEDULE_STATUS_CHOICES else 'Scheduled',
            notes=notes
        )

        db.session.add(schedule)
        db.session.commit()
        flash(f'Shooting schedule added for Scene {scene.scene_number} on {shoot_date} at {call_time}.', 'success')
        return redirect(url_for('schedules.index'))

    preselected_scene_id = request.args.get('scene_id', type=int)
    preselected_film_id = request.args.get('film_id', type=int)

    return render_template(
        'schedules/form.html',
        action='create',
        schedule=None,
        films=films,
        scenes=scenes,
        today_str=today_str,
        preselected_scene_id=preselected_scene_id,
        preselected_film_id=preselected_film_id,
        schedule_statuses=SCHEDULE_STATUS_CHOICES
    )

@schedules_bp.route('/<int:schedule_id>/edit', methods=['GET', 'POST'])
def edit(schedule_id):
    schedule = db.get_or_404(ShootingSchedule, schedule_id)
    films = Film.query.order_by(Film.title.asc()).all()
    scenes = Scene.query.order_by(Scene.film_id.asc(), Scene.scene_number.asc()).all()
    today_str = date.today().isoformat()

    if request.method == 'POST':
        scene_id = request.form.get('scene_id', type=int)
        shoot_date = request.form.get('date', '').strip()
        location = request.form.get('location', '').strip()
        call_time = request.form.get('call_time', '').strip()
        status = request.form.get('status', '').strip()
        notes = request.form.get('notes', '').strip()

        if not scene_id or not shoot_date or not location or not call_time:
            flash('Please fill in all required fields.', 'danger')
            return render_template(
                'schedules/form.html',
                action='edit',
                schedule=schedule,
                films=films,
                scenes=scenes,
                today_str=today_str,
                schedule_statuses=SCHEDULE_STATUS_CHOICES
            )

        scene = db.session.get(Scene, scene_id)
        if scene:
            schedule.scene_id = scene.id
            schedule.film_id = scene.film_id

        schedule.date = shoot_date
        schedule.location = location
        schedule.call_time = call_time
        if status in SCHEDULE_STATUS_CHOICES:
            schedule.status = status
        schedule.notes = notes

        db.session.commit()
        flash('Shooting schedule updated successfully.', 'success')
        return redirect(url_for('schedules.index'))

    return render_template(
        'schedules/form.html',
        action='edit',
        schedule=schedule,
        films=films,
        scenes=scenes,
        today_str=today_str,
        schedule_statuses=SCHEDULE_STATUS_CHOICES
    )

@schedules_bp.route('/<int:schedule_id>/status', methods=['POST'])
def update_status(schedule_id):
    schedule = db.get_or_404(ShootingSchedule, schedule_id)
    new_status = request.form.get('status')
    if new_status in SCHEDULE_STATUS_CHOICES:
        schedule.status = new_status
        db.session.commit()
        flash(f'Call sheet status updated to "{new_status}".', 'info')
    return redirect(request.referrer or url_for('schedules.index'))

@schedules_bp.route('/<int:schedule_id>/delete', methods=['POST'])
def delete(schedule_id):
    schedule = db.get_or_404(ShootingSchedule, schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    flash('Shooting schedule entry removed.', 'info')
    return redirect(url_for('schedules.index'))
