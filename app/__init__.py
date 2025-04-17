from flask import Flask
from flask_login import LoginManager
from .main.routes import main
from .appointment.routes import appointment
from .report.routes import report
from .user.routes import user
from .student.routes import student

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(appointment)
    app.register_blueprint(report)
    app.register_blueprint(user)
    app.register_blueprint(student)
    return app
