from flask import render_template, redirect, url_for, Blueprint
from flask_login import login_required

studentBlueprint = Blueprint("student", __name__, template_folder="templates")

@studentBlueprint.route("/student")
@login_required
def student():
    return render_template("student.html", logo="static/images/logo.PNG", css="static/css/style.css")

@studentBlueprint.route("/students")
@login_required
def students():
    return render_template("students.html", logo="static/images/logo.PNG", css="static/css/style.css")