from flask import Flask
from flask_login import LoginManager
from config import Config
from .main.routes import main
from .appointment.routes import appointmentBlueprint
from .report.routes import reportBlueprint
from .user.routes import user
from .student.routes import studentBlueprint
from .teacher.routes import teacherBlueprint
from .user.user import User
from config import Config

def create_app():
    
    app = Flask(__name__)
<<<<<<< HEAD
    
=======

>>>>>>> 6ed8fded09bf446685bca56de2915c1f28809328
    # Load configuration
    app.config.from_object(Config)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(user_id)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(appointmentBlueprint)
    app.register_blueprint(reportBlueprint)
    app.register_blueprint(user)
    app.register_blueprint(studentBlueprint)
    app.register_blueprint(teacherBlueprint)
    
    return app