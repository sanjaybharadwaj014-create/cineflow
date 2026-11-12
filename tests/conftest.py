import pytest
from app import create_app
from app.config import TestConfig
from app.models import db, Film, Scene, CastCrew, ShootingSchedule

@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for testing."""
    test_app = create_app(TestConfig)

    with test_app.app_context():
        # Clear out any initial seed data so tests have complete control
        db.drop_all()
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def sample_film(app):
    """Creates a sample film for testing."""
    film = Film(
        film_code='FLM-TEST',
        title='Midnight Chronicles',
        director='Helena Morgan',
        genre='Thriller',
        production_status='Shooting',
        start_date='2026-01-10',
        expected_completion_date='2026-06-30',
        synopsis='A secret agent races against the clock.',
        budget='$10,000,000'
    )
    db.session.add(film)
    db.session.commit()
    return film

@pytest.fixture
def sample_scene(app, sample_film):
    """Creates a sample scene associated with sample_film."""
    scene = Scene(
        scene_number='1',
        film_id=sample_film.id,
        location='INT. Control Room',
        characters='Agent Blake, Specialist Vance',
        day_night='INT. NIGHT',
        shooting_date='2026-02-15',
        status='Draft',
        description='Initial satellite intercept.'
    )
    db.session.add(scene)
    db.session.commit()
    return scene

@pytest.fixture
def sample_crew(app, sample_film):
    """Creates a sample cast/crew member."""
    crew = CastCrew(
        film_id=sample_film.id,
        name='Sarah Connor',
        role='Director of Photography',
        department='Camera',
        character='N/A',
        contact='sarah.dp@cineworld.com',
        notes='Dual RED V-Raptor cameras'
    )
    db.session.add(crew)
    db.session.commit()
    return crew

@pytest.fixture
def sample_schedule(app, sample_film, sample_scene):
    """Creates a sample shooting schedule."""
    sched = ShootingSchedule(
        film_id=sample_film.id,
        scene_id=sample_scene.id,
        date='2026-03-01',
        location='Stage 3 Soundstage',
        call_time='07:00 AM',
        status='Scheduled',
        notes='Bring fog machines'
    )
    db.session.add(sched)
    db.session.commit()
    return sched
