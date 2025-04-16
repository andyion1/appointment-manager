from flask import Flask
from config import Config
from flask_login import LoginManager
from models.database import db
from .main.routes import main



def create_app():
    app = Flask(__name__)
    return app
