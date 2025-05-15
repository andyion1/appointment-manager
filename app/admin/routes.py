from math import ceil
from flask import flash, render_template, redirect, request, url_for, Blueprint
from app.user.user import User
from flask_login import current_user, login_required
from models.data_classes import Appointment, Report
from app.admin.forms import AdminCreationForm
from app.admin.forms import AppointmentUpdateForm
from models.database import db
import pdb

adminBlueprint = Blueprint("admin", __name__, template_folder='templates')

@adminBlueprint.route('/admin/users')
@login_required
def list_users():
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    page = int(request.args.get('page', 1))
    per_page = 10
    raw_users = db.get_users()
    if current_user.role == 'admin_user':
        raw_users = [u for u in raw_users if u[5] in ['student', 'teacher']]
    users = [User(*row) for row in raw_users]
    total_pages = ceil(len(users) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    users_paginated = users[start:end]
    return render_template("view-users.html", logo="static/images/logo.PNG", css="static/css/style.css", users=users_paginated, total_pages=total_pages)

@adminBlueprint.route('/users/<int:user_id>')
@login_required
def view_user(user_id):
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    user = db.get_user(f"user_id = {user_id}")
    if current_user.role == 'admin_user' and user.role not in ['student', 'teacher']:
        flash("Access denied", "danger")
        return redirect(url_for('admin.list_users'))
    return render_template("user.html", logo="static/images/logo.PNG", css="static/css/style.css", user=user)


@adminBlueprint.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    if current_user.role == 'admin_user' and current_user.role not in ['student', 'teacher']:
        flash("You cannot modify other admin accounts.", "danger")
        return redirect(url_for('admin.list_users'))
    db.delete_user(user_id)
    flash("User deleted.", "success")
    db.log_admin_action(current_user.user_id, 'delete user', user_id)
    return redirect(url_for('admin.list_users'))

@adminBlueprint.route("/manage_appoint")
@login_required
def manage_appoint():
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied: You do not have permission to view this page.", "danger")
        return redirect(url_for("main.index"))
    page = int(request.args.get('page', 1))
    per_page = 10
    appointments = db.get_appointments_with_details()
    total_pages = ceil(len(appointments) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    appointments_paginated = appointments[start:end]
    return render_template("manage_appoint.html", logo="static/images/logo.PNG", css="static/css/style.css", appointments=appointments_paginated, total_pages=total_pages)

@adminBlueprint.route("/appointments/<int:appointment_id>")
@login_required
def view_appointment(appointment_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    appointment = db.get_appointment_with_details(f"appointment_id = {appointment_id}")
    return render_template("appointment_detail.html", appointment=appointment, logo="static/images/logo.PNG", css="static/css/style.css")

from datetime import datetime, time

@adminBlueprint.route("/appointments/<int:appointment_id>/edit", methods=["GET", "POST"])
@login_required
def edit_appointment(appointment_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied.", "danger")
        return redirect(url_for("main.index"))

    # Get appointment object
    appointment = db.get_appointment_with_details(f"appointment_id = {appointment_id}")
    if not appointment:
        flash("Appointment not found.", "danger")
        return redirect(url_for("admin.manage_appoint"))

    # Create form with populated values
    form = AppointmentUpdateForm(obj=appointment)

    # Populate dropdowns
    form.student_id.choices = [(s.student_id, s.full_name) for s in db.get_students()]
    form.teacher_id.choices = [(t.teacher_id, t.full_name) for t in db.get_teachers()]

    # If form submitted
    if form.validate_on_submit():
        db.update_appointment(appointment_id, {
            'student_id': form.student_id.data,
            'teacher_id': form.teacher_id.data,
            'appointment_date': form.appointment_date.data,
            'appointment_time': form.appointment_time.data,
            'status': form.status.data,
            'reason': form.reason.data
        })
        flash("Appointment updated successfully.", "success")
        return redirect(url_for("admin.manage_appoint"))

    return render_template("appointment_edit.html", form=form, appointment=appointment)



@adminBlueprint.route("/appointments/<int:appointment_id>/delete", methods=["POST"])
@login_required
def delete_appointment(appointment_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied.", "danger")
        return redirect(url_for('main.index'))

    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    if not appointment:
        flash("Appointment not found.", "danger")
        return redirect(url_for("admin.manage_appoint"))

    db.delete_appointment(appointment_id)
    db.log_admin_action(current_user.user_id, f"deleted appointment #{appointment_id}", appointment.student_id)
    flash("Appointment deleted.", "info")
    return redirect(url_for("admin.manage_appoint"))

@adminBlueprint.route('/users/<int:user_id>/warn', methods=['POST'])
@login_required
def warn_user(user_id):
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))
    if current_user.role == 'admin_user' and current_user.role not in ['student', 'teacher']:
        flash("You cannot modify other admin accounts.", "danger")
        return redirect(url_for('admin.list_users'))
    db.update_user(user_id, {'warned': True})
    flash("User has been warned.", "warning")
    db.log_admin_action(current_user.user_id, 'warned user', user_id)
    return redirect(url_for('admin.view_user', user_id=user_id))

@adminBlueprint.route('/users/<int:user_id>/toggle_block', methods=['POST'])
@login_required
def toggle_block_user(user_id):
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    user = db.get_user(f"user_id = {user_id}")
    new_status = 'blocked' if user.status == 'active' else 'active'
    db.update_user(user_id, {'status': new_status})
    flash(f"User has been {'blocked' if new_status == 'blocked' else 'unblocked'}.", "info")
    action = 'blocked user' if new_status == 'blocked' else 'unblocked user'
    db.log_admin_action(current_user.user_id, action, user_id)
    return redirect(url_for('admin.view_user', user_id=user_id))


@adminBlueprint.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != 'admin_super':
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))
    page = int(request.args.get('page', 1))
    per_page = 3
    user_count = len(db.get_users())
    appoint_count = len(db.get_appointments_with_details())
    report_count = len(db.get_reports())
    admin_users = [u for u in db.get_users() if u[5] in ['admin_user', 'admin_appoint', 'admin_super']]  # role at index 5
    total_pages = ceil(len(admin_users) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    admin_users_paginated = admin_users[start:end]
    return render_template("dashboard.html", user_count=user_count, appoint_count=appoint_count, 
        report_count=report_count, admin_users=admin_users_paginated, total_pages=total_pages, css="static/css/style.css", )

@adminBlueprint.route('/manage-reports')
@login_required
def manage_reports():
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    page = int(request.args.get('page', 1))
    per_page = 10
    raw = db.get_reports()
    reports = [Report(*r) for r in raw]
    total_pages = ceil(len(reports) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    reports_paginated = reports[start:end]
    return render_template("manage_reports.html", reports=reports_paginated, total_pages=total_pages, css="static/css/style.css")

@adminBlueprint.route('/reports/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))

    report = db.get_report_with_details(f"report_id = {report_id}")
    if not report:
        flash("Report not found", "danger")
        return redirect(url_for('admin.manage_reports'))

    db.delete_report(report_id)
    db.log_admin_action(current_user.user_id, f"deleted report #{report_id}", report.generated_by)

    flash("Report deleted.", "info")
    return redirect(url_for('admin.manage_reports'))



@adminBlueprint.route("/admin/create", methods=["GET", "POST"])
@login_required
def create_admin():
    if current_user.role != 'admin_super':
        flash("Only superusers can create admin accounts.", "danger")
        return redirect(url_for('admin.dashboard'))

    form = AdminCreationForm()

    if form.validate_on_submit():
        new_admin = User.create_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data
        )
        if new_admin:
            # Log the creation of the new admin
            db.log_admin_action(
                admin_user_id=current_user.user_id,
                action=f"created {form.role.data}",
                target_user_id=new_admin.user_id
            )

            flash(f"Admin '{form.username.data}' created successfully!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("An error occurred. Admin was not created.", "danger")

    return render_template("create_admin.html", form=form, logo="static/images/logo.PNG", css="static/css/style.css")


@adminBlueprint.route('/admin/logs')
@login_required
def view_logs():
    if current_user.role != 'admin_super':
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    logs = db.get_admin_logs()
    return render_template("admin_logs.html", logs=logs)


