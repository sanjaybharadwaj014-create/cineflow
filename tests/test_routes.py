def test_dashboard_route(client, sample_film, sample_scene, sample_schedule):
    """Test dashboard index loads successfully and renders key statistics."""
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Cinema Production Dashboard' in html
    assert 'Total Films' in html
    assert 'Total Scenes' in html
    assert 'Completed Scenes' in html
    assert 'Upcoming Shooting Schedules' in html
    assert 'Current Production Status Breakdown' in html
    assert sample_film.title in html

def test_films_list_route(client, sample_film):
    """Test films listing page."""
    response = client.get('/films/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert sample_film.title in html
    assert sample_film.director in html
    assert sample_film.film_code in html

def test_film_detail_route(client, sample_film, sample_scene):
    """Test film detail page showing scenes and film metadata."""
    response = client.get(f'/films/{sample_film.id}')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert sample_film.title in html
    assert f'Scene {sample_scene.scene_number}' in html

def test_scenes_list_route(client, sample_scene):
    """Test scene management view."""
    response = client.get('/scenes/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert f'Scene {sample_scene.scene_number}' in html
    assert sample_scene.location in html
    assert sample_scene.characters in html

def test_crew_list_route(client, sample_crew):
    """Test cast and crew directory view."""
    response = client.get('/crew/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert sample_crew.name in html
    assert sample_crew.role in html
    assert sample_crew.department in html

def test_schedules_list_route(client, sample_schedule):
    """Test shooting schedule call sheets view."""
    response = client.get('/schedules/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert sample_schedule.call_time in html
    assert sample_schedule.location in html

def test_production_status_route(client, sample_film):
    """Test production pipeline Kanban board view."""
    response = client.get('/production/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Pre-production' in html
    assert 'Shooting' in html
    assert 'Post-production' in html
    assert 'Completed' in html
    assert sample_film.title in html

def test_api_stats_route(client, sample_film, sample_scene):
    """Test API endpoint returning production statistics in JSON format."""
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert 'total_films' in data
    assert 'total_scenes' in data
    assert 'completed_scenes' in data
    assert 'film_status_counts' in data
    assert data['total_films'] >= 1

def test_api_film_scenes_route(client, sample_film, sample_scene):
    """Test API endpoint for retrieving scenes of a specific film."""
    response = client.get(f'/api/films/{sample_film.id}/scenes')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]['scene_number'] == sample_scene.scene_number
