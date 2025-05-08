from datetime import datetime
from flask import render_template, redirect, url_for, Blueprint
from app.appointment.forms import AppointmentForm
from flask_login import current_user, login_required
from models.data_classes import Appointment
from models.database import db
import pdb
from app.user.user import Teacher, Student

appointmentBlueprint = Blueprint("appointment", __name__, template_folder='templates')

@appointmentBlueprint.route("/appointments")
def appointments():
    return render_template("appointments.html", logo="static/images/logo.PNG", css="static/css/style.css")

@appointmentBlueprint.route("/appointment")
def appointment():
    return render_template("appointment.html", logo="static/images/logo.PNG", css="static/css/style.css")

@appointmentBlueprint.route("/bookAppointment", methods=["GET", "POST"])
@login_required
def form():
    form = AppointmentForm()

    teachers = db.get_teachers()
    students = db.get_students()

    students = sorted(students, key=lambda s: s.full_name.lower())
    teachers = sorted(teachers, key=lambda t: t.department.lower() if t.department else "")

    form.teacher.choices = [(t.user_id, f"{t.department} - {t.full_name}") for t in teachers]
    form.student.choices = [(s.user_id, s.full_name) for s in students]

    if form.validate_on_submit():
        if current_user.role == 'student':
            new_appointment = Appointment(
                0,
                Student.get_student_by_user_name(current_user.username).student_id,
                form.teacher.data,
                form.date.data,
                form.time.data,
                "pending",
                form.reason.data,
                datetime.now()
            )
        else:
            new_appointment = Appointment(
                0,
                form.student.data,  # <-- fixed typo
                Teacher.get_teacher_by_user_name(current_user.username).teacher_id,
                form.date.data,
                form.time.data,
                "pending",
                form.reason.data,
                datetime.now()
            )
        db.add_appointment(new_appointment)
        return redirect(url_for('appointment.appointments'))
    else:
        print("Form errors:", form.errors)

    return render_template("book_appointment.html", form=form, logo="static/images/logo.PNG", css="static/css/style.css")
