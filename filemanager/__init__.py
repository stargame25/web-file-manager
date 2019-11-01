from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from secrets import token_hex
from filemanager.config import *
from filemanager.tools import BASE_PATH, valid_upload_dir

default_config = get_config(config_names[0])
WEB_SECTION = default_config.get('web') or []
ENGINE_SECTION = default_config.get('engine') or []
ADMIN_SECTION = default_config.get('admin') or []
DEFAULT_USER = {'username': ADMIN_SECTION.get('username'), 'password': ADMIN_SECTION.get('password')}
FILE_DIR = valid_upload_dir(default_config.get("file_folder"))


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
    app.config['PORT'] = default_config.get("PORT") or 5000
    app.config['DEBUG'] = default_config.get("DEBUG") or False
    app.config['FILE_FOLDER'] = default_config.get("FILE_FOLDER")
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .routes import manager
    app.register_blueprint(manager)

    return app
