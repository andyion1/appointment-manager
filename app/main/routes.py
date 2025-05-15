from math import ceil
from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import current_user
from models.database import db

# Create a blueprint for main routes
main = Blueprint("main", __name__, template_folder='templates')


@main.route("/")
def index():
    """Redirect to home page."""
    return redirect(url_for("main.home"))


@main.route("/home")
def home():
    """
    Display home page with appointment filtering and pagination.
    """
    # Get query parameters
    status_filter = request.args.get('status', 'all')
    page = int(request.args.get('page', 1))
    per_page = 4

    # Retrieve appointments
    appointments = db.get_appointments_by_status(
        status=status_filter if status_filter != 'all' else None
    )

    # Status filter options
    status_options = [
        {'value': 'all', 'label': 'All'},
        {'value': 'pending', 'label': 'Pending'},
        {'value': 'approved', 'label': 'Approved'},
        {'value': 'completed', 'label': 'Completed'},
        {'value': 'cancelled', 'label': 'Cancelled'}
    ]

    # Pagination logic
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
    """Render the about page."""
    return render_template(
        "about.html",
        logo="static/images/logo.PNG",
        css="static/css/style.css"
    )


@main.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors by rendering custom page."""
    return render_template(
        "404.html",
        logo="static/images/logo.PNG",
        css="static/css/style.css"
    ), 404
