from datetime import time
from flask import Blueprint, abort, jsonify, render_template
from models.database import db
import os
from app.extensions import cache
import time

apiBlueprint = Blueprint("api", __name__, template_folder='templates')

@apiBlueprint.route('/api/test-cache')
@cache.cached(timeout=10)
def test_cache():
    """Return current timestamp as JSON to test caching mechanism."""
    return jsonify({"timestamp": time.time()})

@apiBlueprint.route('/api/appointment/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def appointment(id):
    """Get detailed information of a single appointment by ID.
    Returns 404 if not found."""
    appointment = db.get_appointment_with_details(f"appointment_id = {id}")
    if not appointment:
        abort(404, description="appointment not found")
    return jsonify({'result': appointment.to_dict()}), 200

@apiBlueprint.route('/api/report/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def report(id):
    """Get detailed information of a single report by ID.
    Returns 404 if not found."""
    report = db.get_report_with_details(f"report_id = {id}")
    if not report:
        abort(404, description="Report not found")
    return jsonify({'result': report.to_dict()}), 200

@apiBlueprint.route('/api/user/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def user(id):
    """Get detailed information of a single user by ID.
    Returns 404 if not found."""
    user = db.get_user(f"user_id = {id}")
    if not user:
        abort(404, description="user not found")
    return jsonify({'result': user.to_dict()}), 200

@apiBlueprint.route('/api/appointments', methods=['GET'])
@cache.cached(timeout=60)
def appointments():
    """Get a list of all appointments.
    Returns 404 if none found."""
    appointments = db.get_appointments()
    if not appointments:
        abort(404, description="appointments not found")
    return jsonify({'result': [app.to_dict() for app in appointments]}), 200

@apiBlueprint.route('/api/reports', methods=['GET'])
@cache.cached(timeout=60)
def reports():
    """Get a list of all reports.
    Returns 404 if none found."""
    reports = db.get_reports()
    print(type(reports[0]))
    if not reports:
        abort(404, description="Report not found")
    return jsonify({'result': reports}), 200

@apiBlueprint.route('/api/users', methods=['GET'])
@cache.cached(timeout=60)
def users():
    """Get a list of all users.
    Returns 404 if none found."""
    users = db.get_users()
    if not users:
        abort(404, description="user not found")
    return jsonify({'result': users}), 200

@apiBlueprint.route('/api', methods=['GET'])
def api():
    """Render API landing page showing appointments, reports, and users."""
    appointments = db.get_appointments()
    reports = db.get_reports()
    users = db.get_users()
    return render_template("api.html", appointments=appointments, reports=reports, users=users)
