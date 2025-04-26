from flask import render_template, redirect, url_for, Blueprint
from app.appointment.forms import AppointmentForm
from flask_login import current_user, login_required
from models.data_classes import Appointment
from models.database import db

appointment = Blueprint("appointment", __name__, template_folder='templates')

@appointment.route("/appointments")
def home():
    return render_template("appointments.html", logo="static/images/logo.PNG", css="static/css/style.css")

@appointment.route("/appointment")
def about():
    return render_template("appointment.html", logo="static/images/logo.PNG", css="static/css/style.css")

@appointment.route("/bookAppointment")
def form():
    form = AppointmentForm()
    teachers = db.get_teachers()
    form.teacher.choices = [(t.user_id, f"{t.full_name}") for t in teachers]
    if form.validate_on_submit():
        new_appointment = Appointment(
            current_user.id,
            form.teacher.data,
            form.date.data,
            form.time.data,
            form.reason.data,
            'pending'
        )
        
    return render_template("form.html", form=form, logo="static/images/logo.PNG", css="static/css/style.css")