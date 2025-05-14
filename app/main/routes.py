from flask import render_template, redirect, request, url_for, Blueprint
from flask_login import current_user
main = Blueprint("main", __name__, template_folder='templates')
from models.database import db
@main.route("/")
def index():
    return redirect(url_for("main.home"))

@main.route("/home")
def home():
    appointments = db.get_appointments_with_details()
    status_filter = request.args.get('status', 'all')
    
    # Get appointments filtered by status and user role
    appointments = db.get_appointments_by_status(
        status=status_filter if status_filter != 'all' else None,
        user_id=current_user.user_id,
        user_role=current_user.role
    )
    
    # Define available status options for the filter
    status_options = [
        {'value': 'all', 'label': 'All'},
        {'value': 'pending', 'label': 'Pending'},
        {'value': 'approved', 'label': 'Approved'},
        {'value': 'completed', 'label': 'Completed'},
        {'value': 'cancelled', 'label': 'Cancelled'}
    ]
    return render_template("home.html", logo="static/images/logo.PNG", status_filter=status_filter,
        status_options=status_options, css="static/css/style.css",appointments=appointments)

@main.route("/about")
def about():
    return render_template("about.html", logo="static/images/logo.PNG", css="static/css/style.css")

@main.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", logo="static/images/logo.PNG", css="static/css/style.css"), 404