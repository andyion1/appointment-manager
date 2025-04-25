from flask import Flask
from flask_login import LoginManager
from config import Config
from .main.routes import main
from .appointment.routes import appointment
from .report.routes import report
from .user.routes import user
from .student.routes import student
from config import Config

def create_app():
    
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return None
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(appointment)
    app.register_blueprint(report)
    app.register_blueprint(user)
    app.register_blueprint(student)
    
    return app