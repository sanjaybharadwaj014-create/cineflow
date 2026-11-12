from flask import render_template, request, redirect, url_for, flash
from app.blueprints.crew import crew_bp
from app.models import db, CastCrew, Film, DEPARTMENTS

@crew_bp.route('/')
def index():
    dept_filter = request.args.get('department', '').strip()
    film_id = request.args.get('film_id', type=int)
    search_query = request.args.get('q', '').strip()

    query = CastCrew.query

    if dept_filter and dept_filter in DEPARTMENTS:
        query = query.filter_by(department=dept_filter)
    if film_id:
        query = query.filter((CastCrew.film_id == film_id) | (CastCrew.film_id.is_(None)))
    if search_query:
        query = query.filter(
            (CastCrew.name.ilike(f'%{search_query}%')) |
            (CastCrew.role.ilike(f'%{search_query}%')) |
            (CastCrew.character.ilike(f'%{search_query}%')) |
            (CastCrew.contact.ilike(f'%{search_query}%'))
        )

    members = query.order_by(CastCrew.department.asc(), CastCrew.name.asc()).all()
    films = Film.query.order_by(Film.title.asc()).all()

    return render_template(
        'crew/index.html',
        members=members,
        films=films,
        departments=DEPARTMENTS,
        selected_dept=dept_filter,
        selected_film_id=film_id,
        search_query=search_query
    )

@crew_bp.route('/create', methods=['GET', 'POST'])
def create():
    films = Film.query.order_by(Film.title.asc()).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        department = request.form.get('department', '').strip()
        character = request.form.get('character', '').strip()
        contact = request.form.get('contact', '').strip()
        film_id = request.form.get('film_id', type=int)
        notes = request.form.get('notes', '').strip()

        if not name or not role or not department or not contact:
            flash('Please fill in Name, Role, Department, and Contact.', 'danger')
            return render_template(
                'crew/form.html',
                action='create',
                member=None,
                films=films,
                departments=DEPARTMENTS
            )

        if department not in DEPARTMENTS:
            department = 'Production & Logistics'

        # If department is not Cast and character is empty, default to N/A
        if not character:
            character = 'N/A' if department != 'Cast' else 'Lead/Supporting'

        member = CastCrew(
            name=name,
            role=role,
            department=department,
            character=character,
            contact=contact,
            film_id=film_id if film_id else None,
            notes=notes
        )

        db.session.add(member)
        db.session.commit()
        flash(f'Added {name} ({role}) to {department}.', 'success')
        return redirect(url_for('crew.index', department=department))

    preselected_film_id = request.args.get('film_id', type=int)
    preselected_dept = request.args.get('department', '')
    return render_template(
        'crew/form.html',
        action='create',
        member=None,
        films=films,
        departments=DEPARTMENTS,
        preselected_film_id=preselected_film_id,
        preselected_dept=preselected_dept
    )

@crew_bp.route('/<int:member_id>/edit', methods=['GET', 'POST'])
def edit(member_id):
    member = db.get_or_404(CastCrew, member_id)
    films = Film.query.order_by(Film.title.asc()).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        department = request.form.get('department', '').strip()
        character = request.form.get('character', '').strip()
        contact = request.form.get('contact', '').strip()
        film_id = request.form.get('film_id', type=int)
        notes = request.form.get('notes', '').strip()

        if not name or not role or not department or not contact:
            flash('Please fill in Name, Role, Department, and Contact.', 'danger')
            return render_template(
                'crew/form.html',
                action='edit',
                member=member,
                films=films,
                departments=DEPARTMENTS
            )

        member.name = name
        member.role = role
        if department in DEPARTMENTS:
            member.department = department
        member.character = character or ('N/A' if department != 'Cast' else 'Cast')
        member.contact = contact
        member.film_id = film_id if film_id else None
        member.notes = notes

        db.session.commit()
        flash(f'Updated details for {name}.', 'success')
        return redirect(url_for('crew.index', department=member.department))

    return render_template(
        'crew/form.html',
        action='edit',
        member=member,
        films=films,
        departments=DEPARTMENTS
    )

@crew_bp.route('/<int:member_id>/delete', methods=['POST'])
def delete(member_id):
    member = db.get_or_404(CastCrew, member_id)
    name = member.name
    dept = member.department
    db.session.delete(member)
    db.session.commit()
    flash(f'{name} was removed from the roster.', 'info')
    return redirect(url_for('crew.index', department=dept))
