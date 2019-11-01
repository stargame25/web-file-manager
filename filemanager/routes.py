from flask import Blueprint, request, Response, render_template, redirect, url_for, session, flash, send_from_directory, send_file, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from filemanager import db, bcrypt, sitemap, FILE_DIR
from filemanager.tools import *
from filemanager.models import *
from filemanager.forms import *
import qrcode as qr

manager = Blueprint('filemanager', __name__)
file_folder = FILE_DIR
print("File folder", file_folder)

@manager.route(sitemap['home'], methods=['GET', 'POST'])
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
        else:
            flash(u'You were successfully logged in', "Fail")
    return render_template("login.html", theme=generate_theme(session), form=form)


@manager.route(sitemap['offer'], methods=['GET', 'POST'])
def offer_view():
    if current_user.is_authenticated:
        return redirect(url_for('filemanager.transfer_view'))
    return render_template("offer.html", theme=generate_theme(session))


@manager.route(sitemap['transfer'])
@login_required
def transfer_view():
    inputs = TransferInputs()
    return render_template("transfer.html",
                           theme=generate_theme(session), directory=(request.args.get("folder") or ""),
                           prev_directory=os.path.split((request.args.get("folder") or ""))[0], inputs=inputs)


@manager.route(sitemap['qrcode'], methods=["POST"])
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
        return Response(status=404)


@manager.route(sitemap['download'])
@login_required
def download():
    folder = request.args.get("folder")
    file = request.args.get("file")
    if folder is not None and file and file_exists(alt_resource_path(file_folder, folder), file):
        return send_from_directory(alt_resource_path(file_folder, folder), file, as_attachment=True)
    else:
        return Response(status=404)


@manager.route(sitemap['upload'], methods=["POST"])
@login_required
def upload():
    if not request.files and request.args.get("folder"):
        return Response(status=422)
    folder = request.form.get("folder")
    for file in request.files.getlist("files"):
        if file.filename:
            save_file(alt_resource_path(file_folder, folder), file.filename, file.stream.read())
    return Response(status=200)


@manager.route(sitemap['files'], methods=["GET"])
@login_required
def files():
    table = gen_table(alt_resource_path(file_folder, request.args.get("folder")))
    return jsonify(table), 200


@manager.route(sitemap['theme'], methods=['POST'])
def theme_changer():
    data = request.get_json()
    if 'theme' in data.keys() and data.get('theme') in [True, False]:
        session['theme'] = data['theme']
    return Response("", status=200, mimetype='application/json')


@manager.route(sitemap['logout'])
def logout():
    logout_user()
    return redirect(url_for('filemanager.home_view'))
