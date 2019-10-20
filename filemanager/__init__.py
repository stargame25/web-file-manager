from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from secrets import token_hex
import os

BASE_PATH = os.path.abspath(".")
PORT = 5000
DEFAULT_USER = {"login": "admin", "password": "anysecretpassword"}

def resource_path(*args):
    if args:
        return os.path.join(BASE_PATH, *args)
    else:
        return BASE_PATH

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'filemanager.home_view'

sitemap = dict(home='/', offer='/offer', transfer='/transfer', qrcode='/qrcode', download='/download',
               upload='/upload', files='/files', theme='/theme', logout='/logout')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_pyfile(resource_path('filemanager', 'configs', 'config.ini'))
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .routes import manager
    app.register_blueprint(manager)

    return app