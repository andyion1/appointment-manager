from flask import render_template, redirect, url_for, Blueprint, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from .user import User

from .forms import LoginForm, RegistrationForm

# Define the blueprint with the correct name
user = Blueprint("user", __name__, template_folder="templates", static_folder="static")

@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # This would be replaced with actual database query once implemented
            user_login = User.get_user_by_username(form.username.data)
            if user_login.check_password(form.password.data):
                login_user(user_login)
                flash(f'Welcom back, {user_login.full_name}. You have been successfully logged in.', 'info')
                return redirect(url_for('main.home'))
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
                # This would be replaced with actual database insert once implemented
                # For now, just show that the form was successfully submitted
                user_data = User.create_user(form.username.data, form.password.data, form.email.data, form.full_name.data, form.role.data)
                if user_data:
                    flash(f'Registration successful! User {form.username.data} can now log in.', 'success')
                    return redirect(url_for('user.login'))
                
            except Exception as e:
                flash(f'An error occurred during registration.', 'danger')
        else:
            # If form validation fails, display errors
            flash('Registration failed. Please check the form errors.', 'danger')
    
    return render_template("register.html", form=form)

@user.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@user.route("/profile")
def profile():
    return render_template("profile.html")

@user.route("/users")
def users():
    return render_template("users.html")