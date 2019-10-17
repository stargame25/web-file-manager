from flask import Blueprint, request, Response, render_template, redirect, url_for, session, flash, send_from_directory, send_file
from flask_login import login_user, current_user, logout_user, login_required
from filemanager import db, bcrypt, PORT
from filemanager.tools import *
from filemanager.models import *
from filemanager.forms import *
import qrcode as qr

manager = Blueprint('filemanager', __name__)
upload_dir = "files"
file_folder = resource_path(BASE_PATH, upload_dir)


@manager.route('/', methods=['GET', 'POST'])
def home_view():
    if current_user.is_authenticated:
        return redirect(url_for('filemanager.transfer_view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(u'You were successfully logged in', "Success")
            return redirect(url_for('filemanager.transfer_view'))
    return render_template("login.html", theme=generate_theme(session), form=form)


@manager.route('/offer', methods=['GET', 'POST'])
def offer_view():
    if current_user.is_authenticated:
        return redirect(url_for('filemanager.transfer_view'))
    return render_template("offer.html", theme=generate_theme(session))


@manager.route('/transfer')
@login_required
def transfer_view():
    inputs = TransferInputs()
    table = gen_table(file_folder, request.args.get("folder") or "")
    return render_template("transfer.html", theme=generate_theme(session), table=table,
                           directory=(request.args.get("folder") or ""),
                           prev_directory=os.path.split((request.args.get("folder") or ""))[0],
                           inputs=inputs)


@manager.route('/qrcode', methods=["POST"])
@login_required
def qrcode():
    data = request.get_json()
    folder = data.get("folder")
    file = data.get("file")
    if folder is not None and file and file_exists(alt_resource_path(file_folder, folder), file):
        img = qr.make("{0}{1}?folder={2}&file={3}".format(request.host_url.strip("/"), url_for("filemanager.download"),
                                                           data.get("folder"), data.get("file")))
        return send_file(serve_pil_image(img.get_image()), mimetype='image/png', attachment_filename=file,
                         as_attachment=False)
    else:
        return Response(status=422)


@manager.route('/download')
@login_required
def download():
    folder = request.args.get("folder")
    file = request.args.get("file")
    if folder is not None and file and file_exists(alt_resource_path(file_folder, folder), file):
        return send_from_directory(alt_resource_path(file_folder, folder), file, as_attachment=True)
    else:
        return Response(status=422)


@manager.route('/upload', methods=["POST"])
@login_required
def upload():
    if not request.files and request.args.get("folder"):
        return Response(status=500)
    folder = request.args.get("folder")
    for file in request.files:
        save_file(folder, file)
    return Response(status=200)


@manager.route('/theme', methods=['POST'])
def theme_changer():
    data = request.get_json()
    if 'theme' in data.keys() and data.get('theme') in [True, False]:
        session['theme'] = data['theme']
    return Response("", status=200, mimetype='application/json')


@manager.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('filemanager.home_view'))
