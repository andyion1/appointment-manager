import pdb
from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from models.database import db
from .forms import ReportForm
from models.data_classes import Report
from datetime import datetime
from app.user.user import Student, Teacher


reportBlueprint = Blueprint("report", __name__, template_folder='templates')

@reportBlueprint.route("/reports")
@login_required
def view():
    """View all reports created by the current user"""
    cond = f"r.generated_by = {current_user.user_id}"
    reports = db.get_reports_with_details(cond)

    return render_template("reports.html", reports=reports)



@reportBlueprint.route("/report/<int:report_id>")
@login_required
def report(report_id):
    """View a specific report"""
    report = db.get_report_with_details(f"report_id = {report_id}")
    
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('report.view'))

    has_permission = False
    
    if current_user.role in ['admin_appoint', 'superuser']:
        has_permission = True
    elif report.generated_by == current_user.user_id:
        # User can view if they created the report
        has_permission = True

    if not has_permission:
        flash("You don't have permission to view this report", "danger")
        return redirect(url_for('report.view'))

    appointment = db.get_appointment_with_details(f"appointment_id = {report.appointment_id}")
    appointment_details = db.get_appointments_with_details(f"a.appointment_id = {report.appointment_id}")
    
    appointment_detail = appointment_details[0] if appointment_details else None
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
    # Use the improved method to get full appointment details
    appointment = db.get_appointment_with_details(f"a.appointment_id = {appointment_id}")

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
        student = Student.get_student_by_user_name(current_user.username)
        if student and student.student_id == appointment.student_id:
            has_permission = True
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        if teacher and teacher.teacher_id == appointment.teacher_id:
            has_permission = True

    if not has_permission:
        flash("You don't have permission to create a report for this appointment", "danger")
        return redirect(url_for('appointment.appointments'))

    form = ReportForm()

    if form.validate_on_submit():
        # Create a new report
        new_report = Report(
            0,                          # report_id (auto-assigned)
            current_user.user_id,      # generated_by
            form.content.data,         # content
            datetime.now(),            # created_at
            appointment_id,            # appointment_id (correct position)
            form.feedback.data if current_user.role == 'student' else None,
            form.teacher_response.data if current_user.role == 'teacher' else None
        )
        report_id = db.add_report(new_report)

        if report_id:
            flash("Report created successfully!", "success")
            return redirect(url_for('report.report', report_id=report_id))
        else:
            flash("Failed to create report", "danger")

    return render_template(
        "create-report.html",
        form=form,
        appointment=appointment,
        appointment_detail=appointment)



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
    elif report.generated_by == current_user.user_id:
        # Allow update if user created the report
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