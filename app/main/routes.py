from math import ceil
import pdb
from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import current_user
main = Blueprint("main", __name__, template_folder='templates')
from models.database import db
@main.route("/")
def index():
    return redirect(url_for("main.home"))

@main.route("/home")
def home():
    status_filter = request.args.get('status', 'all')
    page = int(request.args.get('page', 1))
    per_page = 4    
    # Pass those values to your DB call (handle None in your DB function accordingly)
    appointments = db.get_appointments_by_status(status=status_filter if status_filter != 'all' else None)
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
        "home.html",
        logo="static/images/logo.PNG",
        status_filter=status_filter,
        status_options=status_options,
        css="static/css/style.css",
        appointments=appointments_paginated,
        total_pages=total_pages
    )


@main.route("/about")
def about():
    return render_template("about.html", logo="static/images/logo.PNG", css="static/css/style.css")

@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", logo="static/images/logo.PNG", css="static/css/style.css"), 404