from flask import render_template, redirect, url_for, Blueprint

user = Blueprint("user", __name__, template_folder="templates")

@user.route("/login")
def login():
    return render_template("login.html", logo="static/images/logo.PNG", css="static/css/style.css")

@user.route("/register")
def register():
    return render_template("register.html", logo="static/images/logo.PNG", css="static/css/style.css")

@user.route("/profile")
def profile():
    return render_template("profile.html", logo="static/images/logo.PNG", css="static/css/style.css")

@user.route("/users")
def users():
    return render_template("users.html", logo="static/images/logo.PNG", css="static/css/style.css")