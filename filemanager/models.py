from flask_login import UserMixin
from filemanager import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    permissions = db.relationship('Permissions', backref='receiver', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

class Permissions(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    object = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False, unique=True)
    subject = db.Column(db.String(64), nullable=False)
    file_name = db.Column(db.String(512), nullable=False)
    size = db.Column(db.String(32), nullable=False)
    date = db.Column(db.String(512), nullable=False, default=datetime.utcnow)
