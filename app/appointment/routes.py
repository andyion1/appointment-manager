from flask import render_template, redirect, url_for, Blueprint
appointment = Blueprint("appointment", __name__, template_folder='templates')

@appointment.route("/appointments")
def home():
    return render_template("appointments.html", logo="static/images/logo.PNG", css="static/css/style.css")

@appointment.route("/appointment")
def about():
    return render_template("appointment.html", logo="static/images/logo.PNG", css="static/css/style.css")