from flask import render_template, redirect, url_for, Blueprint, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from .user import Student, Teacher, User
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
            if user_login and user_login.check_password(form.password.data):
                print("Before Login")
                login_user(user_login)
                print("After  Login")
                flash(f'Welcom back, {user_login.full_name}. You have been successfully logged in.', 'info')
                print("After ")
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
                if user_data:
                    if form.role.data == 'student':
                        return render_template('studentregister.html',form=StudentExtraForm(),user=user_data)
                    elif form.role.data == 'teacher':
                        return render_template('teacherregister.html',form=TeacherExtraForm(),user=user_data)
                
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

    
    if form.validate_on_submit():
        Student.create_student(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email'],
            full_name=request.form['full_name'],
            program=form.program.data,
            student_number=form.student_number.data
        )
        flash("Student registered!", "success")
        return redirect(url_for('user.login'))

    return render_template("studentregister.html", form=form,username=request.form.get('username', ''),email=request.form.get('email', ''),full_name=request.form.get('full_name', ''),password=request.form.get('password', ''))


@user.route("/register/teacher", methods=['GET', 'POST'])
def teacher_register():
    form = TeacherExtraForm()

    if form.validate_on_submit():
        Teacher.create_teacher(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email'],
            full_name=request.form['full_name'],
            department=form.department.data,
            office_location=form.office_location.data
        )
        flash("Teacher registered!", "success")
        return redirect(url_for('user.login'))

    return render_template(
        "teacherregister.html",
        form=form,
        username=request.form.get('username', ''),
        email=request.form.get('email', ''),
        full_name=request.form.get('full_name', ''),
        password=request.form.get('password', '')
    )


@user.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@user.route("/profile", methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        User.update_user(current_user.user_id,form.email.data, form.full_name.data)
        flash(f" updated {request.form['full_name']} with success !", 'success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html', form=form, user=user)


@user.route("/users")
def users():
    return render_template("users.html")