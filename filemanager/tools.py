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
    if "\\" in args:
        r_path = path
        for i in args.split("\\"):
            r_path = os.path.join(r_path, i)
        return r_path
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


def gen_table(files_directory, args):
    pairs = []
    full_path = alt_resource_path(files_directory, args)
    if not os.path.isdir(full_path):
        return None
    list = os.listdir(full_path)
    for file in list:
        location = os.path.join(full_path, file)
        data = os.stat(location)
        isfile = os.path.isfile(location)
        type = "File folder"
        size = ""
        modified = ""
        if isfile:
            size = sizeof_fmt(data.st_size)
            modified = datetime.datetime.fromtimestamp(data.st_mtime).strftime("%Y\%m\%d %H:%M:%S")
            if len(file.split(".")) > 1:
                type = file.split(".")[-1]
            else:
                type = "File"
        created = datetime.datetime.fromtimestamp(data.st_ctime).strftime("%Y\%m\%d %H:%M:%S")
        pairs.append({"name": file, "type": type, "created": created, "modified": modified, "size": size})
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

def save_file(folder, file):
    pass