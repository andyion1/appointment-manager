# Appointment Manager  
### Developed by Andy Ionita, David Hébert, and Joshua Chaisson

A comprehensive Flask web application built collaboratively as a group project.  
The system helps students and teachers efficiently manage academic appointments, featuring secure authentication, scheduling, reporting, and administrative tools — all backed by a PostgreSQL database.

---

## Screenshot


---

## Component Architecture

This application follows a modular Flask structure for scalability and clarity:

- **user/** – authentication, registration, and profile management  
- **appointment/** – appointment creation, modification, and validation  
- **admin/** – administrative tools for managing users, reports, and appointments  
- **report/** – report generation and export functionality  
- **api/** – REST endpoints for integration with external systems  
- **templates/** – Jinja2 HTML templates for all views  
- **static/** – CSS, JavaScript, and image assets  

Each module includes its own routes, forms, and templates to keep responsibilities well separated.

---

## Requirements

### User Authentication
- Secure login and registration using Flask-Login  
- Role-based dashboards for students, teachers, and administrators  
- Password hashing and session management with Werkzeug

### Appointment Management
- Students can book, view, and cancel appointments  
- Teachers can approve, reject, or reschedule appointment requests  
- Built-in time-slot conflict detection  

### Administrative Features
- Manage users, appointments, and reports through an admin panel  
- Generate analytical summaries and reports (REPORT table)  
- Keep an audit trail of admin actions (ADMIN_LOG)

### Database Integration
- PostgreSQL database via SQLAlchemy ORM  
- psycopg2 for database connections  
- Migration support with Flask-Migrate

### Web Interface
- Built with Flask-WTF for forms and CSRF protection  
- Jinja2 templates for dynamic content rendering  
- Responsive layout using standard HTML, CSS, and JavaScript

---

## Additional Information

This web application was developed as a team project for an academic course.  
It is designed for institutions or departments that require structured, role-based scheduling between students and teachers.

- Clear separation of modules and concerns (MVC pattern)  
- Centralized system for appointment management  
- Easily extensible via REST APIs and additional modules  
