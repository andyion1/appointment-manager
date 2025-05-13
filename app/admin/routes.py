from flask import flash, render_template, redirect, request, url_for, Blueprint
from app.user.user import User
from flask_login import current_user, login_required
from models.data_classes import Appointment, Report
from app.admin.forms import AdminCreationForm
from models.database import db
import pdb

adminBlueprint = Blueprint("admin", __name__, template_folder='templates')

@adminBlueprint.route('/admin/users')
@login_required
def list_users():
    if current_user.role not in ['admin_user', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    raw_users = db.get_users()
    if current_user.role == 'admin_user':
        raw_users = [u for u in raw_users if u[5] in ['student', 'teacher']]

    users = [User(*row) for row in raw_users]
    return render_template("view-users.html", logo="static/images/logo.PNG", css="static/css/style.css", users=users)

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
    return redirect(url_for('admin.list_users'))

@adminBlueprint.route("/manage_appoint")
@login_required
def manage_appoint():
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied: You do not have permission to view this page.", "danger")
        return redirect(url_for("main.index"))
    appointments = db.get_appointments_with_details()
    return render_template("manage_appoint.html", logo="static/images/logo.PNG", css="static/css/style.css", appointments=appointments)

@adminBlueprint.route("/appointments/<int:appointment_id>")
@login_required
def view_appointment(appointment_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    return render_template("appointment_detail.html", appointment=appointment, logo="static/images/logo.PNG", css="static/css/style.css")


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
    return redirect(url_for('admin.view_user', user_id=user_id))


@adminBlueprint.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != 'admin_super':
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    user_count = len(db.get_users())
    appoint_count = len(db.get_appointments_with_details())
    report_count = len(db.get_reports())
    admin_users = [u for u in db.get_users() if u[5] in ['admin_user', 'admin_appoint', 'admin_super']]  # role at index 5

    return render_template("dashboard.html", user_count=user_count, appoint_count=appoint_count, report_count=report_count, admin_users=admin_users, logo="static/images/logo.PNG", css="static/css/style.css")

@adminBlueprint.route('/manage-reports')
@login_required
def manage_reports():
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    raw = db.get_reports()
    reports = [Report(*r) for r in raw]
    return render_template("manage_reports.html", reports=reports, logo="static/images/logo.PNG", css="static/css/style.css")

@adminBlueprint.route('/reports/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        content = request.form.get("content")
        db.update_report(report_id, content)
        flash("Report updated.", "success")
        return redirect(url_for('admin.manage_reports'))
    report = db.get_reports(f"report_id = {report_id}")
    return render_template("report_edit.html", report=report[0])


@adminBlueprint.route('/reports/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    if current_user.role not in ['admin_appoint', 'admin_super']:
        flash("Access denied", "danger")
        return redirect(url_for('main.index'))
    db.delete_report(report_id)
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


