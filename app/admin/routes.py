from flask import flash, render_template, redirect, url_for, Blueprint
from app.user.user import User
from flask_login import current_user, login_required
from models.data_classes import Appointment
from models.database import db
import pdb

adminBlueprint = Blueprint("admin", __name__, template_folder='templates')

@adminBlueprint.route('/admin/users')
@login_required
def list_users():
    if current_user.role not in ['admin_user', 'superuser']:
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
    if current_user.role not in ['admin_user', 'superuser']:
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
    if current_user.role not in ['admin_user', 'superuser']:
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
    if current_user.role not in ['admin_appoint', 'superuser']:
        flash("Access denied: You do not have permission to view this page.", "danger")
        return redirect(url_for("main.index"))
    appointments = db.get_appointments_with_details()
    return render_template("manage_appoint.html", logo="static/images/logo.PNG", css="static/css/style.css", appointments=appointments)

@adminBlueprint.route("/appointments/<int:appointment_id>")
@login_required
def view_appointment(appointment_id):
    if current_user.role not in ['admin_appoint', 'superuser']:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    return render_template("appointment_detail.html", appointment=appointment, logo="static/images/logo.PNG", css="static/css/style.css")


@adminBlueprint.route('/users/<int:user_id>/warn', methods=['POST'])
@login_required
def warn_user(user_id):
    if current_user.role not in ['admin_user', 'superuser']:
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
    if current_user.role not in ['admin_user', 'superuser']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    user = db.get_user(f"user_id = {user_id}")
    new_status = 'blocked' if user.status == 'active' else 'active'
    db.update_user(user_id, {'status': new_status})
    flash(f"User has been {'blocked' if new_status == 'blocked' else 'unblocked'}.", "info")
    return redirect(url_for('admin.view_user', user_id=user_id))
