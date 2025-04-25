from flask import render_template, redirect, url_for, Blueprint
report = Blueprint("report", __name__, template_folder='templates')

@report.route("/reports")
def home():
    return render_template("reports.html", logo="static/images/logo.PNG", css="static/css/style.css")

@report.route("/report")
def about():
    return render_template("report.html", logo="static/images/logo.PNG", css="static/css/style.css")