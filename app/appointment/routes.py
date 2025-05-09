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
        student = Student.get_student_by_user_id(current_user.user_id)
        if student:
            appointments = db.get_appointments(f"student_id = {student.student_id}")
        else:
            appointments = []
            
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_id(current_user.user_id)
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
        student = Student.get_student_by_user_id(current_user.user_id)
        if student and student.student_id == appointment.student_id:
            has_permission = True
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_id(current_user.user_id)
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
    
    if current_user.role in ['admin_appoint', 'admin_super']:
        has_permission = True
    elif current_user.role == 'teacher':
        teacher = Teacher.get_teacher_by_user_id(current_user.user_id)
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
    
    # Add debug logging
    print(f"Current user: {current_user.username}, role: {current_user.role}")
    
    teachers = db.get_teachers()
    students = db.get_students()

    # Sort for better UX
    students = sorted(students, key=lambda s: s.full_name.lower())
    teachers = sorted(teachers, key=lambda t: t.department.lower() if t.department else "")

    # Set choices for select fields based on user role
    if current_user.role == 'student' or current_user.role not in ['student', 'teacher']:
        form.teacher.choices = [(t.teacher_id, f"{t.department} - {t.full_name}") for t in teachers]
    
    if current_user.role == 'teacher' or current_user.role not in ['student', 'teacher']:
        form.student.choices = [(s.student_id, s.full_name) for s in students]

    if form.validate_on_submit():
        print("Form validated successfully")
        
        try:
            # Create appointment based on user role
            if current_user.role == 'student':
                student = Student.get_student_by_user_id(current_user.user_id)
                print(f"Found student: {student}")
                
                if student:
                    new_appointment = Appointment(
                        0,  # appointment_id will be assigned by database
                        student.student_id,
                        form.teacher.data,
                        form.date.data,
                        form.time.data,
                        "pending",
                        form.reason.data,
                        datetime.now()
                    )
                    
                    print(f"Trying to add appointment: {vars(new_appointment)}")
                    appointment_id = db.add_appointment(new_appointment)
                    
                    if appointment_id:
                        flash("Appointment created successfully!", "success")
                        return redirect(url_for('appointment.appointments'))
                    else:
                        flash("Failed to create appointment in database", "danger")
                else:
                    flash("Could not find your student record", "danger")
                    
            elif current_user.role == 'teacher':
                # Similar code for teacher role
                teacher = Teacher.get_teacher_by_user_id(current_user.user_id)
                print(f"Found teacher: {teacher}")
                
                if teacher:
                    new_appointment = Appointment(
                        0,
                        form.student.data,
                        teacher.teacher_id,
                        form.date.data,
                        form.time.data,
                        "pending",
                        form.reason.data,
                        datetime.now()
                    )
                    
                    print(f"Trying to add appointment: {vars(new_appointment)}")
                    appointment_id = db.add_appointment(new_appointment)
                    
                    if appointment_id:
                        flash("Appointment created successfully!", "success")
                        return redirect(url_for('appointment.appointments'))
                    else:
                        flash("Failed to create appointment in database", "danger")
                else:
                    flash("Could not find your teacher record", "danger")
            else:
                # Admin path
                new_appointment = Appointment(
                    0,
                    form.student.data,
                    form.teacher.data,
                    form.date.data,
                    form.time.data,
                    "pending",
                    form.reason.data,
                    datetime.now()
                )
                
                print(f"Trying to add appointment: {vars(new_appointment)}")
                appointment_id = db.add_appointment(new_appointment)
                
                if appointment_id:
                    flash("Appointment created successfully!", "success")
                    return redirect(url_for('appointment.appointments'))
                else:
                    flash("Failed to create appointment in database", "danger")
                    
        except Exception as e:
            print(f"Error creating appointment: {e}")
            flash(f"An error occurred: {str(e)}", "danger")
    else:
        # Print form errors for debugging
        if form.errors:
            print("Form errors:", form.errors)

    return render_template("book_appointment.html", form=form)