from flask import render_template, redirect, url_for, Blueprint

student_bp = Blueprint("student", __name__, template_folder="templates")

@student_bp.route("/student")
def index():
    return render_template("student.html", logo="static/images/logo.PNG", css="static/css/style.css")

@student_bp.route("/students")
def student_list():
    return render_template("students.html", logo="static/images/logo.PNG", css="static/css/style.css")