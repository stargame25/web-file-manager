import datetime
import os
from io import BytesIO


BASE_PATH = os.path.abspath(".")


def resource_path(*args):
    if args:
        return os.path.join(BASE_PATH, *args)
    else:
        return BASE_PATH


def alt_resource_path(path, args):
    if args and "\\" in args:
        return os.path.join(path, *(args.split("\\")))
    elif args is None:
        return path
    else:
        return os.path.join(path, args)


def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def generate_theme(session):
    hour = datetime.datetime.now().hour
    if isinstance(session.get("theme"), bool):
        return session.get("theme")
    if hour >= 10 and hour <= 20:
        return False
    return True


def gen_table(files_directory):
    pairs = []
    if not os.path.isdir(files_directory):
        return None
    files_list = os.listdir(files_directory)
    for file in files_list:
        location = os.path.join(files_directory, file)
        data = os.stat(location)
        isfile = os.path.isfile(location)
        ftype = "File folder"
        size = ""
        modified = ""
        if isfile:
            size = sizeof_fmt(data.st_size)
            modified = datetime.datetime.fromtimestamp(data.st_mtime).strftime("%Y\%m\%d %H:%M:%S")
            if len(file.split(".")) > 1:
                ftype = file.split(".")[-1]
            else:
                ftype = "File"
        created = datetime.datetime.fromtimestamp(data.st_ctime).strftime("%Y\%m\%d %H:%M:%S")
        pairs.append({"name": file, "type": ftype, "created": created, "modified": modified, "size": size})
    pairs.sort(key=lambda s: s['created'], reverse=True)
    pairs.sort(key=lambda s: s['type'] == "File folder", reverse=True)
    return pairs


def file_exists(files_directory, file):
    if not os.path.isdir(files_directory):
        return False
    file = resource_path(files_directory, file)
    if os.path.exists(file) and os.path.isfile(file):
        return True
    return False


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


def save_file(files_directory, file_name, file, override=False):
    full_path = resource_path(files_directory, file_name)
    if not os.path.isdir(files_directory):
        return None
    if os.path.exists(full_path) and os.path.isfile(full_path):
        if override:
            with open(full_path, 'wb') as f:
                f.write(file)
        else:
            index = 0
            while os.path.exists(full_path) and os.path.isfile(full_path):
                index += 1
                new_file_name = file_name.split(".")
                new_file_name[0] = new_file_name[0] + " ({0})".format(index)
                new_file_name = ".".join(new_file_name)
                full_path = resource_path(files_directory, new_file_name)
            with open(full_path, 'wb') as f:
                f.write(file)
    else:
        with open(full_path, 'wb') as f:
            f.write(file)


def valid_upload_dir(path):
    if not path:
        path = os.path.join(BASE_PATH, "files")
    if os.path.isdir(path) and os.path.exists(path):
        return path
    else:
        try:
            os.mkdir(path)
            return path
        except Exception:
            return None
