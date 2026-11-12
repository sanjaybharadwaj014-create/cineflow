from datetime import date, timedelta
from app.models import db, Film, Scene, CastCrew, ShootingSchedule

def seed_sample_data():
    """Populate database with rich, realistic cinema production sample data."""
    # Only seed if no films exist
    if Film.query.first():
        return

    today = date.today()
    d_minus_5 = (today - timedelta(days=5)).isoformat()
    d_minus_2 = (today - timedelta(days=2)).isoformat()
    d_today = today.isoformat()
    d_plus_1 = (today + timedelta(days=1)).isoformat()
    d_plus_3 = (today + timedelta(days=3)).isoformat()
    d_plus_7 = (today + timedelta(days=7)).isoformat()
    d_plus_14 = (today + timedelta(days=14)).isoformat()
    d_plus_30 = (today + timedelta(days=30)).isoformat()

    # 1. Create Films
    films_data = [
        Film(
            film_code='FLM-101',
            title='Shadows of Neon',
            director='Christopher Nolan / Sofia Alvarez',
            genre='Sci-Fi / Cyberpunk Noir',
            production_status='Shooting',
            start_date=(today - timedelta(days=20)).isoformat(),
            expected_completion_date=(today + timedelta(days=70)).isoformat(),
            synopsis='In a rain-drenched megacity running on bio-synthetic energy, a rogue cyber-detective uncovers an underworld syndicate tampering with human memories.',
            budget='$18,500,000'
        ),
        Film(
            film_code='FLM-102',
            title='The Last Sunset',
            director='Marcus Sterling',
            genre='Period Drama',
            production_status='Post-production',
            start_date=(today - timedelta(days=120)).isoformat(),
            expected_completion_date=(today + timedelta(days=25)).isoformat(),
            synopsis='A poignant family saga set across the sweeping vineyard estates of northern Italy during the turbulent summer of 1948.',
            budget='$8,200,000'
        ),
        Film(
            film_code='FLM-103',
            title='Echoes of Silence',
            director='Elena Rostova',
            genre='Psychological Mystery',
            production_status='Pre-production',
            start_date=(today + timedelta(days=10)).isoformat(),
            expected_completion_date=(today + timedelta(days=110)).isoformat(),
            synopsis='An acoustic engineer at an isolated mountain observatory begins intercepting strange, rhythmic seismic pulses that correlate with missing townspeople.',
            budget='$4,500,000'
        ),
        Film(
            film_code='FLM-104',
            title='Starlight Odyssey',
            director='Damian Vance',
            genre='Space Adventure',
            production_status='Completed',
            start_date=(today - timedelta(days=280)).isoformat(),
            expected_completion_date=(today - timedelta(days=15)).isoformat(),
            synopsis='The crew of an interstellar deep-survey cruiser must navigate an uncharted gravitational anomaly on the edge of the Perseus Arm.',
            budget='$32,000,000'
        )
    ]

    for f in films_data:
        db.session.add(f)
    db.session.commit()

    f1 = Film.query.filter_by(film_code='FLM-101').first()
    f2 = Film.query.filter_by(film_code='FLM-102').first()
    f3 = Film.query.filter_by(film_code='FLM-103').first()
    f4 = Film.query.filter_by(film_code='FLM-104').first()

    # 2. Create Scenes
    scenes_data = [
        # Film 1: Shadows of Neon (Shooting)
        Scene(
            film_id=f1.id,
            scene_number='1A',
            location='EXT. Neon Alley - District 4',
            characters='Kaelen Thorne, Syndicate Courier',
            day_night='EXT. NIGHT',
            shooting_date=d_minus_5,
            status='Completed',
            description='Kaelen pursues the courier across steam vents and neon-lit fire escapes in torrential rain.'
        ),
        Scene(
            film_id=f1.id,
            scene_number='2',
            location='INT. Kaelen Detective Office',
            characters='Kaelen Thorne, Dr. Maya Lin',
            day_night='INT. NIGHT',
            shooting_date=d_minus_2,
            status='Completed',
            description='Maya brings the decrypted memory chip and warns Kaelen that they have 48 hours.'
        ),
        Scene(
            film_id=f1.id,
            scene_number='3B',
            location='INT. Cybernetics Underground Lab',
            characters='Kaelen Thorne, Viktor Cruz',
            day_night='INT. DAY',
            shooting_date=d_today,
            status='Shooting',
            description='Confrontation with Cruz as the bio-reactor alarms sound in the background.'
        ),
        Scene(
            film_id=f1.id,
            scene_number='4',
            location='EXT. Sky-Bridge Transit Hub',
            characters='Kaelen Thorne, Dr. Maya Lin, Enforcers',
            day_night='EXT. NIGHT',
            shooting_date=d_plus_1,
            status='Scheduled',
            description='High-speed tactical ambush at the automated monorail departure dock.'
        ),
        Scene(
            film_id=f1.id,
            scene_number='5A',
            location='INT. Apex Tower Penthouse',
            characters='Viktor Cruz, Council Board',
            day_night='INT. DAY',
            shooting_date=d_plus_7,
            status='Draft',
            description='The syndicate executives debate executing Protocol Zero.'
        ),
        Scene(
            film_id=f1.id,
            scene_number='6',
            location='EXT. Floodgate Reservoir',
            characters='Kaelen Thorne, Dr. Maya Lin',
            day_night='EXT./INT. DAWN',
            shooting_date=d_plus_14,
            status='Draft',
            description='Final standoff at the reservoir gates as the sunrise breaks through smog.'
        ),

        # Film 2: The Last Sunset (Post-production)
        Scene(
            film_id=f2.id,
            scene_number='1',
            location='EXT. Villa Bellissima Courtyard',
            characters='Gianna Rossi, Matteo Rossi',
            day_night='EXT. DAY',
            shooting_date=(today - timedelta(days=90)).isoformat(),
            status='Completed',
            description='The opening summer celebration and speech commemorating the harvest.'
        ),
        Scene(
            film_id=f2.id,
            scene_number='8C',
            location='INT. Wine Cellar Vault',
            characters='Gianna Rossi, Lorenzo De Luca',
            day_night='INT. NIGHT',
            shooting_date=(today - timedelta(days=60)).isoformat(),
            status='Completed',
            description='Gianna discovers hidden correspondence and sealed ledgers from the war.'
        ),
        Scene(
            film_id=f2.id,
            scene_number='14',
            location='EXT. Sunset Vineyard Overlook',
            characters='Gianna Rossi, Matteo Rossi, Lorenzo',
            day_night='EXT./INT. DUSK',
            shooting_date=(today - timedelta(days=35)).isoformat(),
            status='Completed',
            description='Emotional resolution as the train whistle sounds across the valley.'
        ),

        # Film 3: Echoes of Silence (Pre-production)
        Scene(
            film_id=f3.id,
            scene_number='1',
            location='INT. High-Altitude Acoustic Dome',
            characters='Dr. Arthur Bell, Technician Sarah',
            day_night='INT. NIGHT',
            shooting_date=d_plus_14,
            status='Scheduled',
            description='Arthur isolates the anomalous 14Hz harmonic frequency for the first time.'
        ),
        Scene(
            film_id=f3.id,
            scene_number='2B',
            location='EXT. Pine Ridge Ridge-line',
            characters='Dr. Arthur Bell, Sheriff Wade',
            day_night='EXT. DAY',
            shooting_date=d_plus_30,
            status='Draft',
            description='Sheriff investigates abandoned surveyor vehicle near the perimeter fence.'
        ),

        # Film 4: Starlight Odyssey (Completed)
        Scene(
            film_id=f4.id,
            scene_number='1',
            location='INT. Command Deck - Bridge',
            characters='Captain Mercer, Commander Kira',
            day_night='INT. DAY',
            shooting_date=(today - timedelta(days=200)).isoformat(),
            status='Completed',
            description='Ship enters orbit around the twin neutron stars.'
        ),
        Scene(
            film_id=f4.id,
            scene_number='12',
            location='EXT. Spacewalk Hull Maintenance',
            characters='Commander Kira, Specialist Lee',
            day_night='EXT. NIGHT',
            shooting_date=(today - timedelta(days=150)).isoformat(),
            status='Completed',
            description='Emergency thruster repair during solar flare warning.'
        ),
        Scene(
            film_id=f4.id,
            scene_number='25',
            location='INT. Cryo-Stasis Chamber',
            characters='Captain Mercer',
            day_night='INT. NIGHT',
            shooting_date=(today - timedelta(days=80)).isoformat(),
            status='Completed',
            description='Final log entry before initiating hyper-jump back to Earth orbit.'
        )
    ]

    for s in scenes_data:
        db.session.add(s)
    db.session.commit()

    # 3. Create Cast and Crew
    cast_crew_data = [
        # Cast
        CastCrew(
            film_id=f1.id,
            name='Alexander Vance',
            role='Lead Actor',
            department='Cast',
            character='Kaelen Thorne',
            contact='alex.vance@agencytalent.com / +1-555-0142',
            notes='Stunt double booked for wirework on Scene 4.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Naomi Chen',
            role='Lead Actress',
            department='Cast',
            character='Dr. Maya Lin',
            contact='naomi.chen@cinemarep.com / +1-555-0188',
            notes='Available Mon-Fri. Requires 45-min prosthetic preparation.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Dmitri Volkov',
            role='Supporting Actor',
            department='Cast',
            character='Viktor Cruz',
            contact='dmitri.v@talentmgmt.com / +1-555-0176',
            notes='Lead antagonist. Needs heavy cyber-eye prosthetic.'
        ),
        CastCrew(
            film_id=f2.id,
            name='Alessandra Conti',
            role='Lead Actress',
            department='Cast',
            character='Gianna Rossi',
            contact='aconti@roma-artists.it / +39-06-555123',
            notes='Fluent in Italian and French. Period wardrobe fitted.'
        ),
        CastCrew(
            film_id=f3.id,
            name='Julian Pierce',
            role='Lead Actor',
            department='Cast',
            character='Dr. Arthur Bell',
            contact='j.pierce@theatricalrep.co.uk / +44-20-7946-0912',
            notes='Rehearsal scheduled for next Tuesday.'
        ),

        # Crew - Technical & Creative
        CastCrew(
            film_id=f1.id,
            name='Rodrigo Delgado',
            role='Director of Photography',
            department='Camera',
            character='N/A',
            contact='rodrigo.dp@cinefilms.net / +1-555-0231',
            notes='Operating ARRI Alexa 35 with vintage anamorphic lenses.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Claire Desjardins',
            role='Gaffer / Chief Lighting Technician',
            department='Lighting',
            character='N/A',
            contact='claire.light@cineflow.io / +1-555-0294',
            notes='Specializes in neon RGB and moisture-diffusion lighting rigs.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Tariq Al-Mansoor',
            role='Production Sound Mixer',
            department='Sound',
            character='N/A',
            contact='tariq.sound@audioflow.com / +1-555-0348',
            notes='32-track mobile recording cart, 8 wireless lavaliers.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Hannah Lindqvist',
            role='Production Designer / Art Director',
            department='Art & Props',
            character='N/A',
            contact='hannah.art@scenestudios.com / +1-555-0419',
            notes='Overseeing District 4 neon facades and lab interior set build.'
        ),
        CastCrew(
            film_id=f1.id,
            name='Marcus Brody',
            role='1st Assistant Director (1st AD)',
            department='Direction',
            character='N/A',
            contact='brody1ad@cineflow.io / +1-555-0551',
            notes='Manages daily call sheets, floor operations, and safety.'
        ),
        CastCrew(
            film_id=f2.id,
            name='Evelyn Thorne',
            role='Head of Costume & Wardrobe',
            department='Wardrobe & Makeup',
            character='N/A',
            contact='evelyn.wardrobe@couturefilm.org / +1-555-0612',
            notes='Historical costume authenticity specialist for 1940s Europe.'
        ),
        CastCrew(
            film_id=None,
            name='Rachel Bennett',
            role='Line Producer / Unit Production Manager',
            department='Production & Logistics',
            character='N/A',
            contact='rachel.bennett@cineflow.io / +1-555-0720',
            notes='Studio liaison handling vendor contracts and permits across all projects.'
        )
    ]

    for c in cast_crew_data:
        db.session.add(c)
    db.session.commit()

    # 4. Create Shooting Schedules
    sc1 = Scene.query.filter_by(film_id=f1.id, scene_number='1A').first()
    sc2 = Scene.query.filter_by(film_id=f1.id, scene_number='2').first()
    sc3 = Scene.query.filter_by(film_id=f1.id, scene_number='3B').first()
    sc4 = Scene.query.filter_by(film_id=f1.id, scene_number='4').first()
    sc5 = Scene.query.filter_by(film_id=f1.id, scene_number='5A').first()
    sc_bell = Scene.query.filter_by(film_id=f3.id, scene_number='1').first()

    schedules_data = [
        # Past schedule
        ShootingSchedule(
            film_id=f1.id,
            scene_id=sc1.id,
            date=d_minus_5,
            location='Backlot Alley Stage B (Rain Rig Active)',
            call_time='18:30',
            status='Completed',
            notes='Rain towers enabled. Wet suits provided for camera operators.'
        ),
        ShootingSchedule(
            film_id=f1.id,
            scene_id=sc2.id,
            date=d_minus_2,
            location='Soundstage 4 - Kaelen Office Interior',
            call_time='07:00',
            status='Completed',
            notes='Haze machine safety check passed. Dialogue clarity prioritised.'
        ),
        # Today's schedule
        ShootingSchedule(
            film_id=f1.id,
            scene_id=sc3.id,
            date=d_today,
            location='Industrial Warehouse B - Underground Lab Set',
            call_time='06:30',
            status='In Progress',
            notes='Stunt fight rehearsal at 07:15. Fire marshal on set for sparking reactor prop.'
        ),
        # Upcoming schedules
        ShootingSchedule(
            film_id=f1.id,
            scene_id=sc4.id,
            date=d_plus_1,
            location='Sky-Bridge Transit Deck - Stage 7 (Blue Screen)',
            call_time='08:00',
            status='Scheduled',
            notes='Motion-control crane rig on track. VFX markers placed on rear screen.'
        ),
        ShootingSchedule(
            film_id=f1.id,
            scene_id=sc5.id,
            date=d_plus_7,
            location='Highrise Corporate Tower - 42nd Floor Suite',
            call_time='09:00',
            status='Scheduled',
            notes='Strict noise protocol. Elevator access pass required for all grip crew.'
        ),
        ShootingSchedule(
            film_id=f3.id,
            scene_id=sc_bell.id,
            date=d_plus_14,
            location='Mount Wilson Observatory - Main Dome',
            call_time='19:00',
            status='Scheduled',
            notes='Night exterior shoot. Thermal jackets mandatory for all technical crew.'
        )
    ]

    for s in schedules_data:
        db.session.add(s)
    db.session.commit()
