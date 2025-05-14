from flask import render_template, redirect, url_for, Blueprint
main = Blueprint("main", __name__, template_folder='templates')
from models.database import db
@main.route("/")
def index():
    return redirect(url_for("main.home"))

@main.route("/home")
def home():
    appointments = db.get_appointments_with_details()
    return render_template("home.html", logo="static/images/logo.PNG", css="static/css/style.css",appointments=appointments)

@main.route("/about")
def about():
    return render_template("about.html", logo="static/images/logo.PNG", css="static/css/style.css")

@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", logo="static/images/logo.PNG", css="static/css/style.css"), 404