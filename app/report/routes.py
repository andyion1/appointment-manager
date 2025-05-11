from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from models.database import db
from .forms import ReportForm
from models.data_classes import Report
from datetime import datetime

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

@reportBlueprint.route("/appointment/<int:appointment_id>/report/create", methods=["GET", "POST"])
@login_required
def create(appointment_id):
    """Create a new report for an appointment"""
    # Check if the appointment exists
    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))
    
    # Check if a report already exists for this appointment
    existing_report = db.get_report(f"appointment_id = {appointment_id}")
    if existing_report:
        flash("A report already exists for this appointment", "info")
        return redirect(url_for('report.report', report_id=existing_report.report_id))
    
    # Check permissions
    has_permission = False
    
    if current_user.role in ['admin_appoint', 'superuser']:
        has_permission = True
    elif current_user.role == 'student':
        student = db.get_student(f"user_id = {current_user.user_id}")
        if student and student.student_id == appointment.student_id:
            has_permission = True
    elif current_user.role == 'teacher':
        teacher = db.get_teacher(f"user_id = {current_user.user_id}")
        if teacher and teacher.teacher_id == appointment.teacher_id:
            has_permission = True
    
    if not has_permission:
        flash("You don't have permission to create a report for this appointment", "danger")
        return redirect(url_for('appointment.appointments'))
    
    form = ReportForm()
    
    if form.validate_on_submit():
        # Create a new report
        new_report = Report(
            0,                          # report_id (will be auto-assigned)
            appointment_id,             # appointment_id
            current_user.user_id,       # generated_by
            form.content.data,          # content
            datetime.now(),             # created_at
            form.feedback.data if current_user.role == 'student' else None,  # feedback (only if student)
            form.teacher_response.data if current_user.role == 'teacher' else None  # teacher_response (only if teacher)
        )
        
        report_id = db.add_report(new_report)
        
        if report_id:
            flash("Report created successfully!", "success")
            return redirect(url_for('report.report', report_id=report_id))
        else:
            flash("Failed to create report", "danger")
    
    # Get appointment details for the form
    appointment_details = db.get_appointments_with_details(f"a.appointment_id = {appointment_id}")
    
    if appointment_details:
        appointment_detail = appointment_details[0]
    else:
        appointment_detail = None
    
    return render_template(
        "create_report.html",
        form=form,
        appointment=appointment,
        appointment_detail=appointment_detail)


@reportBlueprint.route("/report/<int:report_id>/update", methods=["POST"])
@login_required
def update(report_id):
    """Update an existing report"""
    report = db.get_report(f"report_id = {report_id}")
    
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('report.view'))
    
    # Check permissions
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
        flash("You don't have permission to update this report", "danger")
        return redirect(url_for('report.view'))
    
    form = ReportForm()
    
    if form.validate_on_submit():
        updates = {
            'content': form.content.data
        }
        
        # Only update feedback if user is a student or admin
        if current_user.role == 'student' or current_user.role in ['admin_appoint', 'superuser']:
            updates['feedback'] = form.feedback.data
        
        # Only update teacher_response if user is a teacher or admin
        if current_user.role == 'teacher' or current_user.role in ['admin_appoint', 'superuser']:
            updates['teacher_response'] = form.teacher_response.data
        
        success = db.update_report(report_id, updates)
        
        if success:
            flash("Report updated successfully!", "success")
        else:
            flash("Failed to update report", "danger")
    
    return redirect(url_for('report.report', report_id=report_id))

@reportBlueprint.route("/report/<int:report_id>/delete", methods=["POST"])
@login_required
def delete(report_id):
    """Delete a report"""
    # Only admin users can delete reports
    if current_user.role not in ['admin_appoint', 'superuser']:
        flash("You don't have permission to delete reports", "danger")
        return redirect(url_for('report.view'))
    
    success = db.delete_report(report_id)
    
    if success:
        flash("Report deleted successfully!", "success")
    else:
        flash("Failed to delete report", "danger")
    
    return redirect(url_for('report.view'))