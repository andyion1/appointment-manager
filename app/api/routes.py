from datetime import time
from flask import Blueprint, abort, jsonify, render_template
from models.database import db
import os
from app.extensions import cache
import time
apiBlueprint = Blueprint("api", __name__, template_folder='templates')

# Get a single author (GET /api/author/<id>)
@apiBlueprint.route('/api/test-cache')
@cache.cached(timeout=10)
def test_cache():
    return jsonify({"timestamp": time.time()})

@apiBlueprint.route('/api/appointment/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def appointment(id):
    appointment = db.get_appointment(f"appointment_id = {id}")
    if not appointment:
        abort(404, description="appointment not found") 
    return jsonify({'result': appointment}), 200
@apiBlueprint.route('/api/report/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def report(id):
    report = db.get_report_with_details(f"report_id = {id}")
    if not report:
        abort(404, description="Report not found") 
    return jsonify({'result': report}), 200
@apiBlueprint.route('/api/user/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def user(id):
    user = db.get_user(f"user_id = {id}")
    if not user:
        abort(404, description="user not found") 
    return jsonify({'result': user}), 200
@apiBlueprint.route('/api/appointments', methods=['GET'])
@cache.cached(timeout=60)
def get_appointments():
    appointments = db.get_appointments() 
    result = []
    for app in appointments:
        result.append({
            "appointment_id": app.appointment_id,
            "date": app.date,
            "user_id": app.user_id,
            # add whatever fields you want to expose
        })

    return jsonify({'result': result}), 200
@apiBlueprint.route('/api/reports', methods=['GET'])
@cache.cached(timeout=60)
def reports():
    reports = db.get_reports()
    if not reports:
        abort(404, description="Report not found") 
    return jsonify({'result': reports}), 200
@apiBlueprint.route('/api/users', methods=['GET'])
@cache.cached(timeout=60)
def users():
    users = db.get_users()
    if not users:
        abort(404, description="user not found") 
    return jsonify({'result': users}), 200
# Default API landing route
@apiBlueprint.route('/api', methods=['GET'])
def api():
    return render_template("api.html")