from filemanager import db, bcrypt, create_app, PORT, DEFAULT_USER
from filemanager.models import User

app = create_app()

def database_init(app):
    with app.app_context():
        db.create_all()
        if db.session.query(User).filter_by(username='admin').count() < 1:
            admin_user = User(username=DEFAULT_USER['login'],
                              password=bcrypt.generate_password_hash(DEFAULT_USER['password']))
            db.session.add(admin_user)
            db.session.commit()


if __name__ == '__main__':
    database_init(app)
    app.run('0.0.0.0', debug=True, port=PORT)
