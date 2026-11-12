from flask import render_template, request, redirect, url_for, flash
from app.blueprints.films import films_bp
from app.models import db, Film, Scene, CastCrew, ShootingSchedule, PRODUCTION_STATUS_CHOICES

@films_bp.route('/')
def index():
    status_filter = request.args.get('status', '').strip()
    search_query = request.args.get('q', '').strip()

    query = Film.query

    if status_filter and status_filter in PRODUCTION_STATUS_CHOICES:
        query = query.filter_by(production_status=status_filter)

    if search_query:
        query = query.filter(
            (Film.title.ilike(f'%{search_query}%')) |
            (Film.director.ilike(f'%{search_query}%')) |
            (Film.genre.ilike(f'%{search_query}%')) |
            (Film.film_code.ilike(f'%{search_query}%'))
        )

    films = query.order_by(Film.id.desc()).all()

    return render_template(
        'films/index.html',
        films=films,
        status_filter=status_filter,
        search_query=search_query,
        production_statuses=PRODUCTION_STATUS_CHOICES
    )

@films_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        film_code = request.form.get('film_code', '').strip().upper()
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        genre = request.form.get('genre', '').strip()
        production_status = request.form.get('production_status', 'Pre-production').strip()
        start_date = request.form.get('start_date', '').strip()
        expected_completion_date = request.form.get('expected_completion_date', '').strip()
        synopsis = request.form.get('synopsis', '').strip()
        budget = request.form.get('budget', '').strip()

        # Validation
        if not title or not director or not genre or not start_date or not expected_completion_date:
            flash('Please fill in all required fields.', 'danger')
            return render_template(
                'films/form.html',
                action='create',
                film=None,
                production_statuses=PRODUCTION_STATUS_CHOICES
            )

        # Auto-generate film_code if missing
        if not film_code:
            count = Film.query.count() + 1
            film_code = f'FLM-{count:03d}'
        else:
            existing = Film.query.filter_by(film_code=film_code).first()
            if existing:
                flash(f'Film ID "{film_code}" already exists. Please use a unique identifier.', 'danger')
                return render_template(
                    'films/form.html',
                    action='create',
                    film=None,
                    production_statuses=PRODUCTION_STATUS_CHOICES
                )

        if production_status not in PRODUCTION_STATUS_CHOICES:
            production_status = 'Pre-production'

        film = Film(
            film_code=film_code,
            title=title,
            director=director,
            genre=genre,
            production_status=production_status,
            start_date=start_date,
            expected_completion_date=expected_completion_date,
            synopsis=synopsis,
            budget=budget
        )

        db.session.add(film)
        db.session.commit()
        flash(f'Film "{title}" ({film_code}) created successfully!', 'success')
        return redirect(url_for('films.detail', film_id=film.id))

    return render_template(
        'films/form.html',
        action='create',
        film=None,
        production_statuses=PRODUCTION_STATUS_CHOICES
    )

@films_bp.route('/<int:film_id>')
def detail(film_id):
    film = db.get_or_404(Film, film_id)
    scenes = Scene.query.filter_by(film_id=film.id).order_by(Scene.scene_number.asc()).all()
    crew_members = CastCrew.query.filter((CastCrew.film_id == film.id) | (CastCrew.film_id.is_(None))).order_by(CastCrew.department.asc(), CastCrew.name.asc()).all()
    schedules = ShootingSchedule.query.filter_by(film_id=film.id).order_by(ShootingSchedule.date.asc(), ShootingSchedule.call_time.asc()).all()

    return render_template(
        'films/detail.html',
        film=film,
        scenes=scenes,
        crew_members=crew_members,
        schedules=schedules,
        production_statuses=PRODUCTION_STATUS_CHOICES
    )

@films_bp.route('/<int:film_id>/edit', methods=['GET', 'POST'])
def edit(film_id):
    film = db.get_or_404(Film, film_id)

    if request.method == 'POST':
        film_code = request.form.get('film_code', '').strip().upper()
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        genre = request.form.get('genre', '').strip()
        production_status = request.form.get('production_status', 'Pre-production').strip()
        start_date = request.form.get('start_date', '').strip()
        expected_completion_date = request.form.get('expected_completion_date', '').strip()
        synopsis = request.form.get('synopsis', '').strip()
        budget = request.form.get('budget', '').strip()

        if not title or not director or not genre or not start_date or not expected_completion_date:
            flash('Please fill in all required fields.', 'danger')
            return render_template(
                'films/form.html',
                action='edit',
                film=film,
                production_statuses=PRODUCTION_STATUS_CHOICES
            )

        if film_code and film_code != film.film_code:
            existing = Film.query.filter_by(film_code=film_code).first()
            if existing and existing.id != film.id:
                flash(f'Film ID "{film_code}" already exists for another film.', 'danger')
                return render_template(
                    'films/form.html',
                    action='edit',
                    film=film,
                    production_statuses=PRODUCTION_STATUS_CHOICES
                )
            film.film_code = film_code

        film.title = title
        film.director = director
        film.genre = genre
        if production_status in PRODUCTION_STATUS_CHOICES:
            film.production_status = production_status
        film.start_date = start_date
        film.expected_completion_date = expected_completion_date
        film.synopsis = synopsis
        film.budget = budget

        db.session.commit()
        flash(f'Film "{title}" updated successfully!', 'success')
        return redirect(url_for('films.detail', film_id=film.id))

    return render_template(
        'films/form.html',
        action='edit',
        film=film,
        production_statuses=PRODUCTION_STATUS_CHOICES
    )

@films_bp.route('/<int:film_id>/delete', methods=['POST'])
def delete(film_id):
    film = db.get_or_404(Film, film_id)
    title = film.title
    db.session.delete(film)
    db.session.commit()
    flash(f'Film "{title}" and all related scenes and schedules were removed.', 'info')
    return redirect(url_for('films.index'))
