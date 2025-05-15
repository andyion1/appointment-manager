from datetime import datetime
from math import ceil
from flask import render_template, redirect, url_for, Blueprint, flash, request
from app.appointment.forms import AppointmentForm, AppointmentStatusForm, AppointmentUpdateForm
from flask_login import current_user, login_required
from models.data_classes import Appointment
from models.database import db
import pdb
from app.user.user import Teacher, Student

appointmentBlueprint = Blueprint("appointment", __name__, template_folder='templates')

@appointmentBlueprint.route("/appointments")
@login_required
def appointments():
    """Display paginated list of appointments filtered by user role and status."""
    page = int(request.args.get('page', 1))
    per_page = 4 
    if current_user.role == 'student':
        student = Student.get_student_by_user_name(current_user.username)
        if student:
            appointments = db.get_appointments_with_details(f"s.student_id = {student.student_id}")
        else:
            appointments = []
            
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_name(current_user.username)
        if teacher:
            appointments = db.get_appointments_with_details(f"t.teacher_id = {teacher.teacher_id}")
        else:
            appointments = []
            
    elif current_user.role in ['admin_appoint', 'admin_super']:
        appointments = db.get_appointments_with_details()
        
    else:
        appointments = []
    status_filter = request.args.get('status', 'all')
    
    appointments = db.get_appointments_by_status(
        status=status_filter if status_filter != 'all' else None,
        user_id=current_user.user_id,
        user_role=current_user.role
    )
    
    status_options = [
        {'value': 'all', 'label': 'All'},
        {'value': 'pending', 'label': 'Pending'},
        {'value': 'approved', 'label': 'Approved'},
        {'value': 'completed', 'label': 'Completed'},
        {'value': 'cancelled', 'label': 'Cancelled'}
    ]

    total_pages = ceil(len(appointments) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    appointments_paginated = appointments[start:end]

    return render_template(
        "appointments.html", 
        appointments=appointments_paginated, 
        status_filter=status_filter,
        status_options=status_options,
        total_pages=total_pages
    )

@appointmentBlueprint.route("/appointment/<int:appointment_id>", methods=["GET", "POST"])
@login_required
def appointment(appointment_id):
    """Show and optionally update details of a specific appointment if authorized."""
    appointment = db.get_appointment_with_details(f"a.appointment_id = {appointment_id}")
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))

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

    report = db.get_report_with_details(f"appointment_id = {appointment.appointment_id}")
    form = AppointmentUpdateForm()
    base_status_choices = [
        ('approved', 'Approved'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    if appointment.created_role == current_user.role:
        base_status_choices = [choice for choice in base_status_choices if choice[0] != 'approved']

    form.status.choices = base_status_choices
    if form.validate_on_submit():
        updates = {}

        date_changed = form.appointment_date.data != appointment.appointment_date
        time_changed = form.appointment_time.data != appointment.appointment_time

        if date_changed:
            updates['appointment_date'] = form.appointment_date.data
        if time_changed:
            updates['appointment_time'] = form.appointment_time.data

        if date_changed or time_changed:
            updates['status'] = "pending"
        elif form.status.data:
            updates['status'] = form.status.data

        if form.reason.data:
            updates['reason'] = form.reason.data

        if updates:
            db.update_appointment(appointment_id, updates)
            flash("Appointment updated successfully!", "success")
        else:
            flash("No changes detected.", "info")

        return redirect(url_for('appointment.appointment', appointment_id=appointment_id))

    if request.method == "GET":
        form.appointment_date.data = appointment.appointment_date
        form.appointment_time.data = appointment.appointment_time
        form.status.data = appointment.status
        form.reason.data = appointment.reason
    return render_template("appointment.html", appointment=appointment, form=form, report=report)

@appointmentBlueprint.route("/appointment/<int:appointment_id>/status", methods=["POST"])
@login_required
def update_status(appointment_id):
    """Update status of an appointment if the current user is authorized."""
    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('appointment.appointments'))
    
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
    """Display and process appointment booking form for students and teachers."""
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
                datetime.now(),
                'student'
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
                datetime.now(),
                'teacher'
            )
        db.add_appointment(new_appointment)
        return redirect(url_for('appointment.appointments'))
    else:
        print("Form errors:", form.errors)

    return render_template("book_appointment.html", form=form, logo="static/images/logo.PNG", css="static/css/style.css")
