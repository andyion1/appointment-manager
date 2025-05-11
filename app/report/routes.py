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


@reportBlueprint.route("/report/<int:report_id>")
@login_required
def report(report_id):
    """View a specific report"""
    report = db.get_report(f"report_id = {report_id}")
    
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('report.view'))
    
    # Check if user has permission to view this report
    has_permission = False
    
    if current_user.role in ['admin_appoint', 'superuser']:
        has_permission = True
    else:
        # Get the appointment related to this report
        appointment = db.get_appointment(f"appointment_id = {report.appointment_id}")
        
        if appointment:
            if current_user.role == 'student':
                student = db.get_student(f"user_id = {current_user.user_id}")
                if student and student.student_id == appointment.student_id:
                    has_permission = True
            elif current_user.role == 'teacher':
                teacher = db.get_teacher(f"user_id = {current_user.user_id}")
                if teacher and teacher.teacher_id == appointment.teacher_id:
                    has_permission = True
    
    if not has_permission:
        flash("You don't have permission to view this report", "danger")
        return redirect(url_for('report.view'))
    
    # Get the related appointment, student, and teacher info
    appointment = db.get_appointment(f"appointment_id = {report.appointment_id}")
    appointment_details = db.get_appointments_with_details(f"a.appointment_id = {report.appointment_id}")
    
    if appointment_details:
        appointment_detail = appointment_details[0]
    else:
        appointment_detail = None
    
    # Create form for updating report
    form = ReportForm(obj=report)
    
    return render_template(
        "report.html",
        report=report,
        appointment=appointment,
        appointment_detail=appointment_detail,
        form=form
    )