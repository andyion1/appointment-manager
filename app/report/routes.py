from flask import render_template, redirect, url_for, Blueprint
from flask_login import login_required
reportBlueprint = Blueprint("report", __name__, template_folder='templates')

@reportBlueprint.route("/reports")
def reports():
    return render_template("reports.html", logo="static/images/logo.PNG", css="static/css/style.css")

@reportBlueprint.route("/report")
def report():
    return render_template("report.html", logo="static/images/logo.PNG", css="static/css/style.css")

@reportBlueprint.route("/createReport")
@login_required
def createReport():
    return render_template("createReport.html", logo="static/images/logo.PNG", css="static/css/style.css")