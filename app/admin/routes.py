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
    users = [User(*row) for row in raw_users]
    return render_template("view-users.html", logo="static/images/logo.PNG", css="static/css/style.css", users=users)

@adminBlueprint.route('/users/<int:user_id>')
@login_required
def view_user(user_id):
    if current_user.role not in ['admin_user', 'superuser']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    user = db.get_user(f"user_id = {user_id}")
    return render_template("user.html", logo="static/images/logo.PNG", css="static/css/style.css", user=user)


@adminBlueprint.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role not in ['admin_user', 'superuser']:
        flash("Access denied", "danger")
        return redirect(url_for('main.home'))

    db.delete_user(user_id)
    flash("User deleted.", "success")
    return render_template("appointments.html", logo="static/images/logo.PNG", css="static/css/style.css")