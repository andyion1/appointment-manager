from flask import render_template, redirect, session, url_for, Blueprint, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

from models.utils import save_file
from .user import Student, Teacher, User
from werkzeug.utils import secure_filename
from flask import current_app
from models.database import db
import pdb

from .forms import LoginForm, RegistrationForm, ProfileForm, StudentExtraForm, TeacherExtraForm

# Define the blueprint with the correct name
user = Blueprint("user", __name__, template_folder="templates", static_folder="static")

@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # This would be replaced with actual database query once implemented
            user_login = User.get_user_by_username(form.username.data)
            if user_login:
                if user_login.status == 'blocked':
                    flash("Your account has been blocked. Please contact an administrator.", "danger")
                    return redirect(url_for('user.login'))
                
                if user_login.check_password(form.password.data):
                    login_user(user_login)
                    flash(f'Welcome back, {user_login.full_name}. You have been successfully logged in.', 'info')
                    return redirect(url_for('user.profile'))
        else:
            # If form validation fails, display errors
            flash('Login failed. Please check the form errors.', 'danger')
    
    return render_template("login.html", form=form)

@user.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_data = User.create_user(form.username.data, form.password.data, form.email.data, form.full_name.data, form.role.data)
                session['user'] = {
                    'username': form.username.data,
                    'password': form.password.data,
                    'email': form.email.data,
                    'full_name': form.full_name.data,
                    'role': form.role.data
                }
                if user_data:
                    if form.role.data == 'student':
                        return redirect(url_for('user.student_register'))
                    elif form.role.data == 'teacher':
                        return redirect(url_for('user.teacher_register'))
                
            except Exception as e:
                flash(f'An error occurred during registration.', 'danger')
                print("Registration error:", e)
        else:
            # If form validation fails, display errors
            flash('Registration failed. Please check the form errors.', 'danger')
    
    return render_template("register.html", form=form)

@user.route("/register/student", methods=['GET', 'POST'])
def student_register():
    form = StudentExtraForm()
    user = session.get('user')
    if not user:
        return redirect(url_for('user.register'))
    
    if form.validate_on_submit():
        Student.create_student(
            username=user['username'],
            password=user['password'],
            email=user['email'],
            full_name=user['full_name'],
            program=form.program.data,
            student_number=form.student_number.data
        )
        flash("Student registered!", "success")
        return redirect(url_for('user.login'))

    return render_template("studentregister.html", form=form)


@user.route("/register/teacher", methods=['GET', 'POST'])
def teacher_register():
    form = TeacherExtraForm()
    user = session.get('user')
    if not user:
        return redirect(url_for('user.register'))
    
    if form.validate_on_submit():
        Teacher.create_teacher(
            username=user['username'],
            password=user['password'],
            email=user['email'],
            full_name=user['full_name'],
            department=form.department.data,
            office_location=form.office_location.data
        )
        flash("Teacher registered!", "success")
        return redirect(url_for('user.login'))

    return render_template("teacherregister.html",form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@user.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    # Get user object directly
    user_obj = User.get_user_by_id(current_user.user_id)

    # Preload form with user data
    form = ProfileForm(obj=user_obj)

    # Default image path (for displaying if needed)
    user_image = current_user.user_image  # Assumes this field exists on User
    if form.validate_on_submit():
        # Check if a new image was uploaded
        if form.user_image.data:
            # Save image and get new filename
            new_file_name = save_file(form.user_image.data)  # You must define save_file()  
            user_image = new_file_name  # Update the image path

        # Update user info in the DB
        updates = {}
        updates['email'] = form.email.data
        updates['full_name'] = form.full_name.data
        updates['user_image'] = user_image  # Include new image filename if uploaded}
        db.update_user(current_user.user_id, updates)  # Make sure db.update_user accepts a dict

        flash(f"Profile updated successfully!", 'success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html', form=form)



@user.route("/users")
@login_required
def users():
    return render_template("users.html")