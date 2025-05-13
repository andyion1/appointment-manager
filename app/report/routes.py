import pdb
from flask import render_template, redirect, request, url_for, Blueprint, flash
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
    if current_user.role == 'teacher':
        teacher = db.get_teacher_by_user_name(current_user.username)
        if teacher:
            reports = db.get_reports_with_details(f"a.teacher_id = {teacher.teacher_id}")
        else:
            flash("Teacher profile not found.", "danger")
            reports = []
    elif current_user.role in ['admin_appoint', 'admin_super', 'student']:
        reports = db.get_reports_with_details()
    else:
        flash("Access denied.", "danger")
        return redirect(url_for("main.index"))

    return render_template("reports.html", reports=reports)


@reportBlueprint.route("/report/<int:report_id>")
@login_required
def report(report_id):
    # Get report from DB
    form = ReportForm()
    report = db.get_report_with_details(f"report_id = {report_id}")
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for("report.view"))

    # Only allow access to relevant users
    has_permission = False

    if current_user.role in ['admin_super', 'admin_appoint']:
        has_permission = True
    elif current_user.role == 'student':
        student = Student.get_student_by_user_name(current_user.username)
        if student and student.student_id == student.student_id:
            has_permission = True
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        appointment = db.get_appointment(f"appointment_id = {report.appointment_id}")
        if teacher and appointment and teacher.teacher_id == appointment.teacher_id:
            has_permission = True

    if not has_permission:
        flash("You don't have permission to view this report", "danger")
        return redirect(url_for("report.view"))

    return render_template("report.html", report=report, form=form)



@reportBlueprint.route("/appointment/<int:appointment_id>/report/create", methods=["GET", "POST"])
@login_required
def create(appointment_id):
    """Create a new report for an appointment"""
    appointment = db.get_appointment_with_details(f"a.appointment_id = {appointment_id}")

    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))

    existing_report = db.get_report_with_details(f"appointment_id = {appointment_id}")
    if existing_report:
        flash("A report already exists for this appointment", "info")
        return redirect(url_for('report.report', report_id=existing_report.report_id))

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
        new_report = Report(
            report_id=0,
            generated_by=current_user.user_id,
            created_at=datetime.now(),
            appointment_id=appointment_id,
            feedback=form.feedback.data if current_user.role == 'student' else None,
            teacher_response=form.teacher_response.data if current_user.role == 'teacher' else None
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
        appointment_detail=appointment
    )

@reportBlueprint.route("/report/<int:report_id>/update", methods=["POST"])
@login_required
def update(report_id):
    """Update an existing report"""
    report = db.get_report_with_details(f"report_id = {report_id}")

    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('report.view'))

    has_permission = False

    # Admins can always edit
    if current_user.role in ['admin_appoint', 'admin_super']:
        has_permission = True

    # Students who created the report can edit
    elif report.generated_by == current_user.user_id:
        has_permission = True

    # Teacher who handled the appointment (match on name)
    elif current_user.role == 'teacher' and report.teacher_name == current_user.full_name:
        has_permission = True

    if not has_permission:
        flash("You don't have permission to update this report", "danger")
        return redirect(url_for('report.view'))
    created_at = {}
    if current_user.role in ['admin_appoint', 'admin_super']:
        created_at["feedback"] = request.form.get("feedback")
        created_at["teacher_response"] = request.form.get("teacher_response")
    elif current_user.role == 'student' and report.generated_by == current_user.user_id:
        created_at["feedback"] = request.form.get("feedback")
    elif current_user.role == 'teacher' and report.teacher_name == current_user.full_name:
        created_at["teacher_response"] = request.form.get("teacher_response")

    created_at["created_at"] = datetime.now()

    db.update_report(report_id, created_at)

    flash("Report updated successfully", "success")
    return redirect(url_for('report.view'))



@reportBlueprint.route("/report/<int:report_id>/delete", methods=["POST"])
@login_required
def delete(report_id):
    """Delete a report"""
    if current_user.role not in ['admin_appoint', 'superuser']:
        flash("You don't have permission to delete reports", "danger")
        return redirect(url_for('report.view'))

    db.delete_report(report_id)
    flash("Report deleted successfully!", "success")

    return redirect(url_for('report.view'))
