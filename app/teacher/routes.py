from math import ceil
from flask import abort, render_template, redirect, request, url_for, Blueprint
from models.database import db

teacherBlueprint = Blueprint("teacher", __name__, template_folder="templates")

@teacherBlueprint.route("/teachers/<int:teacher_id>")
def teacher(teacher_id):
    """Return a specific teacher's profile page."""
    teacher = db.get_teacher(f"teacher_id = {teacher_id}")
    if not teacher:
        abort(404)
    return render_template("teacher.html", logo="static/images/logo.PNG", css="static/css/style.css", teacher=teacher)

@teacherBlueprint.route("/teachers")
def teachers():
    """Return a paginated list of all teachers."""
    page = int(request.args.get('page', 1))
    per_page = 3
    teachers = db.get_teachers()
    total_pages = ceil(len(teachers) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    teachers_paginated = teachers[start:end]
    return render_template("teachers.html", total_pages=total_pages, css="static/css/style.css", teachers=teachers_paginated)
