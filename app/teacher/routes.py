from flask import abort, render_template, redirect, url_for, Blueprint
from models.database import db

teacherBlueprint = Blueprint("teacher", __name__, template_folder="templates")

@teacherBlueprint.route("/teachers/<int:teacher_id>")
def teacher(teacher_id):
    teacher = db.get_teacher(f"teacher_id = {teacher_id}")
    if not teacher:
        abort(404)
    return render_template("teacher.html", logo="static/images/logo.PNG", css="static/css/style.css", teacher=teacher)

@teacherBlueprint.route("/teachers")
def teachers():
    teachers = db.get_teachers()
    return render_template("teachers.html", logo="static/images/logo.PNG", css="static/css/style.css", teachers=teachers)