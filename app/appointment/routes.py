from datetime import datetime
from flask import render_template, redirect, url_for, Blueprint, flash, request
from app.appointment.forms import AppointmentForm, AppointmentStatusForm
from flask_login import current_user, login_required
from models.data_classes import Appointment
from models.database import db
import pdb
from app.user.user import Teacher, Student

appointmentBlueprint = Blueprint("appointment", __name__, template_folder='templates')

@appointmentBlueprint.route("/appointments")
@login_required
def appointments():
    # Get appointments based on user role
    if current_user.role == 'student':
        student = Student.get_student_by_user_name(current_user.username)
        if student:
            appointments = db.get_appointments(f"student_id = {student.student_id}")
        else:
            appointments = []
            
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        if teacher:
            appointments = db.get_appointments(f"teacher_id = {teacher.teacher_id}")
        else:
            appointments = []
            
    elif current_user.role in ['admin_appoint', 'admin_super']:
        # Admins can see all appointments
        appointments = db.get_appointments()
        
    else:
        appointments = []
    
    return render_template("appointments.html", appointments=appointments)

@appointmentBlueprint.route("/appointment/<int:appointment_id>")
@login_required
def appointment(appointment_id):
    # Get the appointment
    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))
    
    # Check if user has permission to view this appointment
    has_permission = False
    
    if current_user.role in ['admin_appoint', 'admin_super']:
        has_permission = True
    elif current_user.role == 'student':
        student = Student.get_student_by_user_name(current_user.username)
        if student and student.student_id == appointment.student_id:
            has_permission = True
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        if teacher and teacher.teacher_id == appointment.teacher_id:
            has_permission = True
    
    if not has_permission:
        flash("You don't have permission to view this appointment", "danger")
        return redirect(url_for('appointment.appointments'))
    
    # Get the related teacher and student info using the database methods
    teacher = db.get_teacher(f"teacher_id = {appointment.teacher_id}")
    student = db.get_student(f"student_id = {appointment.student_id}")
    
    # Create status form for updating appointment status
    form = AppointmentStatusForm()
    
    return render_template(
        "appointment.html",
        appointment=appointment,
        teacher=teacher,
        student=student,
        status_form=form
    )

@appointmentBlueprint.route("/appointment/<int:appointment_id>/status", methods=["POST"])
@login_required
def update_status(appointment_id):
    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))
    
    # Check permissions
    has_permission = False
    
    if current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        if teacher and teacher.teacher_id == appointment.teacher_id:
            has_permission = True
    
    if not has_permission:
        flash("You don't have permission to update this appointment's status", "danger")
        return redirect(url_for('appointment.appointments'))
    
    form = AppointmentStatusForm()
    
    if form.validate_on_submit():
        updates = {
            'status': form.status.data
        }
        
        db.update_appointment(appointment_id, updates)
        flash("Appointment status updated successfully!", "success")
    
    return redirect(url_for('appointment.appointment', appointment_id=appointment_id))

@appointmentBlueprint.route("/bookAppointment", methods=["GET", "POST"])
@login_required
def form():
    form = AppointmentForm()

    teachers = db.get_teachers()
    students = db.get_students()

    students = sorted(students, key=lambda s: s.full_name.lower())
    teachers = sorted(teachers, key=lambda t: t.department.lower() if t.department else "")

    form.teacher.choices = [(t.teacher_id, f"{t.department} - {t.full_name}") for t in teachers]
    form.student.choices = [(s.student_id, s.full_name) for s in students]

    print("Current user:", current_user.username)
    print("teacher data:", form.teacher.data)
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
                form.student.data,
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
