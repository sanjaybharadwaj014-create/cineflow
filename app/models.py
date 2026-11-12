from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Constant choices for validation and dropdowns
PRODUCTION_STATUS_CHOICES = [
    'Pre-production',
    'Shooting',
    'Post-production',
    'Completed'
]

SCENE_STATUS_CHOICES = [
    'Draft',
    'Scheduled',
    'Shooting',
    'Completed'
]

DAY_NIGHT_CHOICES = [
    'INT. DAY',
    'INT. NIGHT',
    'EXT. DAY',
    'EXT. NIGHT',
    'EXT./INT. DUSK',
    'EXT./INT. DAWN'
]

DEPARTMENTS = [
    'Direction',
    'Cast',
    'Camera',
    'Lighting',
    'Sound',
    'Art & Props',
    'Wardrobe & Makeup',
    'Production & Logistics',
    'Post-Production / VFX'
]

SCHEDULE_STATUS_CHOICES = [
    'Scheduled',
    'In Progress',
    'Completed',
    'Postponed',
    'Cancelled'
]


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    film_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    production_status = db.Column(db.String(30), default='Pre-production', nullable=False)
    start_date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    expected_completion_date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    synopsis = db.Column(db.Text, nullable=True)
    budget = db.Column(db.String(50), nullable=True)

    # Relationships
    scenes = db.relationship('Scene', backref='film', lazy=True, cascade='all, delete-orphan')
    crew_members = db.relationship('CastCrew', backref='film', lazy=True)
    schedules = db.relationship('ShootingSchedule', backref='film', lazy=True, cascade='all, delete-orphan')

    @property
    def total_scenes(self):
        return len(self.scenes)

    @property
    def completed_scenes(self):
        return len([s for s in self.scenes if s.status == 'Completed'])

    @property
    def progress_percentage(self):
        if not self.scenes:
            if self.production_status == 'Completed':
                return 100
            elif self.production_status == 'Post-production':
                return 75
            elif self.production_status == 'Shooting':
                return 40
            return 10
        return round((self.completed_scenes / self.total_scenes) * 100)

    def to_dict(self):
        return {
            'id': self.id,
            'film_code': self.film_code,
            'title': self.title,
            'director': self.director,
            'genre': self.genre,
            'production_status': self.production_status,
            'start_date': self.start_date,
            'expected_completion_date': self.expected_completion_date,
            'synopsis': self.synopsis or '',
            'budget': self.budget or '',
            'total_scenes': self.total_scenes,
            'completed_scenes': self.completed_scenes,
            'progress_percentage': self.progress_percentage
        }


class Scene(db.Model):
    __tablename__ = 'scenes'

    id = db.Column(db.Integer, primary_key=True)
    scene_number = db.Column(db.String(20), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    characters = db.Column(db.String(250), nullable=False)
    day_night = db.Column(db.String(30), nullable=False)  # e.g., 'INT. DAY', 'EXT. NIGHT'
    shooting_date = db.Column(db.String(10), nullable=True)  # Format: YYYY-MM-DD
    status = db.Column(db.String(30), default='Draft', nullable=False)  # Draft, Scheduled, Shooting, Completed
    description = db.Column(db.Text, nullable=True)

    # Relationships
    schedules = db.relationship('ShootingSchedule', backref='scene', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'scene_number': self.scene_number,
            'film_id': self.film_id,
            'film_title': self.film.title if self.film else '',
            'location': self.location,
            'characters': self.characters,
            'day_night': self.day_night,
            'shooting_date': self.shooting_date or '',
            'status': self.status,
            'description': self.description or ''
        }


class CastCrew(db.Model):
    __tablename__ = 'cast_crew'

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    character = db.Column(db.String(100), default='N/A')
    contact = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'film_id': self.film_id,
            'film_title': self.film.title if self.film else 'All Productions',
            'name': self.name,
            'role': self.role,
            'department': self.department,
            'character': self.character or 'N/A',
            'contact': self.contact,
            'notes': self.notes or ''
        }


class ShootingSchedule(db.Model):
    __tablename__ = 'shooting_schedules'

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'), nullable=False)
    scene_id = db.Column(db.Integer, db.ForeignKey('scenes.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    location = db.Column(db.String(150), nullable=False)
    call_time = db.Column(db.String(20), nullable=False)  # e.g., '06:30 AM', '14:00'
    status = db.Column(db.String(30), default='Scheduled', nullable=False)  # Scheduled, In Progress, Completed, Postponed, Cancelled
    notes = db.Column(db.Text, nullable=True)

    @property
    def is_upcoming(self):
        today_str = date.today().isoformat()
        return self.date >= today_str and self.status in ['Scheduled', 'In Progress']

    def to_dict(self):
        return {
            'id': self.id,
            'film_id': self.film_id,
            'film_title': self.film.title if self.film else '',
            'scene_id': self.scene_id,
            'scene_number': self.scene.scene_number if self.scene else '',
            'date': self.date,
            'location': self.location,
            'call_time': self.call_time,
            'status': self.status,
            'notes': self.notes or ''
        }
