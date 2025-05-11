from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from models.database import db

reportBlueprint = Blueprint("report", __name__, template_folder='templates')

@reportBlueprint.route("/reports")
@login_required
def view():
    """View all reports that the current user has access to"""
    if current_user.role == 'student':
        # Students can only see reports for their appointments
        student = db.get_student(f"user_id = {current_user.user_id}")
        if student:
            cond = f"r.appointment_id IN (SELECT appointment_id FROM APPOINTMENT WHERE student_id = {student.student_id})"
            reports = db.get_reports_with_details(cond)
        else:
            reports = []
    elif current_user.role == 'teacher':
        # Teachers can only see reports for their appointments
        teacher = db.get_teacher(f"user_id = {current_user.user_id}")
        if teacher:
            cond = f"r.appointment_id IN (SELECT appointment_id FROM APPOINTMENT WHERE teacher_id = {teacher.teacher_id})"
            reports = db.get_reports_with_details(cond)
        else:
            reports = []
    elif current_user.role in ['admin_appoint', 'superuser']:
        # Admin users can see all reports
        reports = db.get_reports_with_details()
    else:
        reports = []
    
    return render_template("reports.html", reports=reports)