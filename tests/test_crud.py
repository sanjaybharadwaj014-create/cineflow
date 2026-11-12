from app.models import db, Film, Scene, CastCrew, ShootingSchedule

def test_create_and_edit_film(client):
    """Test creating a new film and then updating its fields."""
    # 1. Create Film
    create_resp = client.post('/films/create', data={
        'film_code': 'FLM-CRUD1',
        'title': 'Neon Horizon',
        'director': 'Elena Rostov',
        'genre': 'Cyberpunk',
        'production_status': 'Pre-production',
        'start_date': '2026-06-01',
        'expected_completion_date': '2026-11-30',
        'synopsis': 'High-tech neo-noir thriller.',
        'budget': '$12,000,000'
    }, follow_redirects=True)
    assert create_resp.status_code == 200

    film = Film.query.filter_by(film_code='FLM-CRUD1').first()
    assert film is not None
    assert film.title == 'Neon Horizon'

    # 2. Edit Film
    edit_resp = client.post(f'/films/{film.id}/edit', data={
        'film_code': 'FLM-CRUD1',
        'title': 'Neon Horizon: Director Cut',
        'director': 'Elena Rostov',
        'genre': 'Cyberpunk / Action',
        'production_status': 'Shooting',
        'start_date': '2026-06-01',
        'expected_completion_date': '2026-12-15',
        'synopsis': 'Updated logline.',
        'budget': '$14,000,000'
    }, follow_redirects=True)
    assert edit_resp.status_code == 200

    updated = db.session.get(Film, film.id)
    assert updated.title == 'Neon Horizon: Director Cut'
    assert updated.production_status == 'Shooting'

def test_create_and_delete_scene(client, sample_film):
    """Test creating and deleting a scene."""
    # 1. Create Scene
    resp = client.post('/scenes/create', data={
        'scene_number': '5B',
        'film_id': sample_film.id,
        'location': 'EXT. Rooftop Helipad',
        'characters': 'Jack, Elena',
        'day_night': 'EXT. NIGHT',
        'shooting_date': '2026-03-20',
        'status': 'Draft',
        'description': 'Helicopter evacuation scene.'
    }, follow_redirects=True)
    assert resp.status_code == 200

    scene = Scene.query.filter_by(scene_number='5B', film_id=sample_film.id).first()
    assert scene is not None
    assert scene.location == 'EXT. Rooftop Helipad'

    # 2. Update Scene Status
    status_resp = client.post(f'/scenes/{scene.id}/status', data={
        'status': 'Completed'
    }, follow_redirects=True)
    assert status_resp.status_code == 200
    assert db.session.get(Scene, scene.id).status == 'Completed'

    # 3. Delete Scene
    del_resp = client.post(f'/scenes/{scene.id}/delete', follow_redirects=True)
    assert del_resp.status_code == 200
    assert db.session.get(Scene, scene.id) is None

def test_create_and_edit_crew(client, sample_film):
    """Test creating and modifying a crew member."""
    resp = client.post('/crew/create', data={
        'name': 'Lucas Scott',
        'role': 'Gaffer',
        'department': 'Lighting',
        'character': 'N/A',
        'contact': 'lucas.gaffer@light.com',
        'film_id': sample_film.id,
        'notes': 'Experienced with high-voltage exterior rigs'
    }, follow_redirects=True)
    assert resp.status_code == 200

    member = CastCrew.query.filter_by(name='Lucas Scott').first()
    assert member is not None
    assert member.role == 'Gaffer'
    assert member.department == 'Lighting'

    # Delete crew
    del_resp = client.post(f'/crew/{member.id}/delete', follow_redirects=True)
    assert del_resp.status_code == 200
    assert db.session.get(CastCrew, member.id) is None

def test_create_and_edit_schedule(client, sample_film, sample_scene):
    """Test creating and managing shooting schedule."""
    resp = client.post('/schedules/create', data={
        'scene_id': sample_scene.id,
        'date': '2026-04-10',
        'location': 'Soundstage A - Main Set',
        'call_time': '06:00 AM',
        'status': 'Scheduled',
        'notes': 'Stunt team required at 06:30 AM'
    }, follow_redirects=True)
    assert resp.status_code == 200

    sched = ShootingSchedule.query.filter_by(scene_id=sample_scene.id).first()
    assert sched is not None
    assert sched.call_time == '06:00 AM'

    # Update schedule status
    status_resp = client.post(f'/schedules/{sched.id}/status', data={
        'status': 'In Progress'
    }, follow_redirects=True)
    assert status_resp.status_code == 200
    assert db.session.get(ShootingSchedule, sched.id).status == 'In Progress'

def test_production_stage_update(client, sample_film):
    """Test updating the production stage via the production pipeline."""
    assert sample_film.production_status == 'Shooting'

    resp = client.post(f'/production/update-stage/{sample_film.id}', data={
        'production_status': 'Post-production'
    }, follow_redirects=True)
    assert resp.status_code == 200

    film = db.session.get(Film, sample_film.id)
    assert film.production_status == 'Post-production'
