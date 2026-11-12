from app.models import db, Film, Scene, CastCrew, ShootingSchedule

def test_create_film(app):
    """Test Film model creation and properties."""
    film = Film(
        film_code='FLM-999',
        title='Solar Winds',
        director='David Miller',
        genre='Sci-Fi',
        production_status='Pre-production',
        start_date='2026-05-01',
        expected_completion_date='2026-12-01',
        synopsis='A deep space exploratory flight.',
        budget='$25,000,000'
    )
    db.session.add(film)
    db.session.commit()

    saved_film = Film.query.filter_by(film_code='FLM-999').first()
    assert saved_film is not None
    assert saved_film.title == 'Solar Winds'
    assert saved_film.director == 'David Miller'
    assert saved_film.production_status == 'Pre-production'
    assert saved_film.total_scenes == 0
    assert saved_film.completed_scenes == 0
    assert saved_film.progress_percentage == 10  # fallback for pre-production with no scenes

def test_scene_progress_calculation(app, sample_film):
    """Test scene completion rate calculation on Film."""
    scene1 = Scene(
        scene_number='1',
        film_id=sample_film.id,
        location='INT. Station',
        characters='Hero',
        day_night='INT. DAY',
        status='Completed'
    )
    scene2 = Scene(
        scene_number='2',
        film_id=sample_film.id,
        location='EXT. Station',
        characters='Hero, Villain',
        day_night='EXT. NIGHT',
        status='Shooting'
    )
    db.session.add_all([scene1, scene2])
    db.session.commit()

    assert sample_film.total_scenes == 2
    assert sample_film.completed_scenes == 1
    assert sample_film.progress_percentage == 50

def test_cast_crew_model(app, sample_film):
    """Test CastCrew model fields and dictionary serialization."""
    actor = CastCrew(
        film_id=sample_film.id,
        name='Emma Stone',
        role='Lead Actress',
        department='Cast',
        character='Agent Vance',
        contact='emma@agency.com'
    )
    db.session.add(actor)
    db.session.commit()

    saved = CastCrew.query.filter_by(name='Emma Stone').first()
    assert saved is not None
    assert saved.role == 'Lead Actress'
    assert saved.department == 'Cast'
    assert saved.character == 'Agent Vance'
    assert saved.film.title == sample_film.title

    data = saved.to_dict()
    assert data['name'] == 'Emma Stone'
    assert data['character'] == 'Agent Vance'

def test_shooting_schedule_model(app, sample_film, sample_scene):
    """Test ShootingSchedule relationship with Film and Scene."""
    sched = ShootingSchedule(
        film_id=sample_film.id,
        scene_id=sample_scene.id,
        date='2026-10-15',
        location='Alleyway Soundstage',
        call_time='06:30 AM',
        status='Scheduled',
        notes='High speed camera rig'
    )
    db.session.add(sched)
    db.session.commit()

    saved = ShootingSchedule.query.filter_by(location='Alleyway Soundstage').first()
    assert saved is not None
    assert saved.film.id == sample_film.id
    assert saved.scene.scene_number == sample_scene.scene_number
    assert saved.call_time == '06:30 AM'
    assert saved.status == 'Scheduled'

def test_cascade_delete_film(app, sample_film, sample_scene, sample_schedule):
    """Deleting a film should cascade delete its scenes and schedules."""
    film_id = sample_film.id
    scene_id = sample_scene.id
    schedule_id = sample_schedule.id

    db.session.delete(sample_film)
    db.session.commit()

    assert db.session.get(Film, film_id) is None
    assert db.session.get(Scene, scene_id) is None
    assert db.session.get(ShootingSchedule, schedule_id) is None
