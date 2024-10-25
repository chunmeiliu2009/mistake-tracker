import os
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create unique filename to prevent overwrites
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    return None
