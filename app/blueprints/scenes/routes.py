from flask import render_template, request, redirect, url_for, flash, jsonify
from app.blueprints.scenes import scenes_bp
from app.models import (
    db, Scene, Film,
    SCENE_STATUS_CHOICES, DAY_NIGHT_CHOICES
)

@scenes_bp.route('/')
def index():
    film_id = request.args.get('film_id', type=int)
    status_filter = request.args.get('status', '').strip()
    day_night_filter = request.args.get('day_night', '').strip()
    search_query = request.args.get('q', '').strip()

    query = Scene.query

    if film_id:
        query = query.filter_by(film_id=film_id)
    if status_filter and status_filter in SCENE_STATUS_CHOICES:
        query = query.filter_by(status=status_filter)
    if day_night_filter and day_night_filter in DAY_NIGHT_CHOICES:
        query = query.filter_by(day_night=day_night_filter)
    if search_query:
        query = query.filter(
            (Scene.scene_number.ilike(f'%{search_query}%')) |
            (Scene.location.ilike(f'%{search_query}%')) |
            (Scene.characters.ilike(f'%{search_query}%')) |
            (Scene.description.ilike(f'%{search_query}%'))
        )

    scenes = query.order_by(Scene.film_id.asc(), Scene.scene_number.asc()).all()
    films = Film.query.order_by(Film.title.asc()).all()

    return render_template(
        'scenes/index.html',
        scenes=scenes,
        films=films,
        selected_film_id=film_id,
        status_filter=status_filter,
        day_night_filter=day_night_filter,
        search_query=search_query,
        scene_statuses=SCENE_STATUS_CHOICES,
        day_night_choices=DAY_NIGHT_CHOICES
    )

@scenes_bp.route('/create', methods=['GET', 'POST'])
def create():
    films = Film.query.order_by(Film.title.asc()).all()

    if request.method == 'POST':
        scene_number = request.form.get('scene_number', '').strip()
        film_id = request.form.get('film_id', type=int)
        location = request.form.get('location', '').strip()
        characters = request.form.get('characters', '').strip()
        day_night = request.form.get('day_night', 'INT. DAY').strip()
        shooting_date = request.form.get('shooting_date', '').strip()
        status = request.form.get('status', 'Draft').strip()
        description = request.form.get('description', '').strip()

        if not scene_number or not film_id or not location or not characters or not day_night:
            flash('Please fill in all required scene details (Scene #, Film, Location, Characters, Day/Night).', 'danger')
            return render_template(
                'scenes/form.html',
                action='create',
                scene=None,
                films=films,
                scene_statuses=SCENE_STATUS_CHOICES,
                day_night_choices=DAY_NIGHT_CHOICES
            )

        film = db.session.get(Film, film_id)
        if not film:
            flash('Selected film does not exist.', 'danger')
            return redirect(url_for('scenes.create'))

        scene = Scene(
            scene_number=scene_number,
            film_id=film_id,
            location=location,
            characters=characters,
            day_night=day_night,
            shooting_date=shooting_date if shooting_date else None,
            status=status if status in SCENE_STATUS_CHOICES else 'Draft',
            description=description
        )

        db.session.add(scene)
        db.session.commit()
        flash(f'Scene {scene_number} added to "{film.title}".', 'success')
        return redirect(url_for('scenes.index', film_id=film.id))

    preselected_film_id = request.args.get('film_id', type=int)
    return render_template(
        'scenes/form.html',
        action='create',
        scene=None,
        films=films,
        preselected_film_id=preselected_film_id,
        scene_statuses=SCENE_STATUS_CHOICES,
        day_night_choices=DAY_NIGHT_CHOICES
    )

@scenes_bp.route('/<int:scene_id>/edit', methods=['GET', 'POST'])
def edit(scene_id):
    scene = db.get_or_404(Scene, scene_id)
    films = Film.query.order_by(Film.title.asc()).all()

    if request.method == 'POST':
        scene_number = request.form.get('scene_number', '').strip()
        film_id = request.form.get('film_id', type=int)
        location = request.form.get('location', '').strip()
        characters = request.form.get('characters', '').strip()
        day_night = request.form.get('day_night', '').strip()
        shooting_date = request.form.get('shooting_date', '').strip()
        status = request.form.get('status', '').strip()
        description = request.form.get('description', '').strip()

        if not scene_number or not film_id or not location or not characters or not day_night:
            flash('Please fill in all required fields.', 'danger')
            return render_template(
                'scenes/form.html',
                action='edit',
                scene=scene,
                films=films,
                scene_statuses=SCENE_STATUS_CHOICES,
                day_night_choices=DAY_NIGHT_CHOICES
            )

        scene.scene_number = scene_number
        scene.film_id = film_id
        scene.location = location
        scene.characters = characters
        scene.day_night = day_night
        scene.shooting_date = shooting_date if shooting_date else None
        if status in SCENE_STATUS_CHOICES:
            scene.status = status
        scene.description = description

        db.session.commit()
        flash(f'Scene {scene.scene_number} updated successfully.', 'success')
        return redirect(url_for('scenes.index', film_id=scene.film_id))

    return render_template(
        'scenes/form.html',
        action='edit',
        scene=scene,
        films=films,
        scene_statuses=SCENE_STATUS_CHOICES,
        day_night_choices=DAY_NIGHT_CHOICES
    )

@scenes_bp.route('/<int:scene_id>/status', methods=['POST'])
def update_status(scene_id):
    scene = db.get_or_404(Scene, scene_id)
    new_status = request.form.get('status')
    if new_status in SCENE_STATUS_CHOICES:
        scene.status = new_status
        db.session.commit()
        flash(f'Scene {scene.scene_number} marked as "{new_status}".', 'info')
    return redirect(request.referrer or url_for('scenes.index'))

@scenes_bp.route('/<int:scene_id>/delete', methods=['POST'])
def delete(scene_id):
    scene = db.get_or_404(Scene, scene_id)
    film_id = scene.film_id
    scene_num = scene.scene_number
    db.session.delete(scene)
    db.session.commit()
    flash(f'Scene {scene_num} deleted.', 'info')
    return redirect(url_for('scenes.index', film_id=film_id))
