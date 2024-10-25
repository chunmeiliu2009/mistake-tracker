import os
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            print(f"Creating upload directory: {UPLOAD_FOLDER}")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create unique filename to prevent overwrites
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                filename = f"{base}_{counter}{ext}"
                counter += 1
                
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(f"Saving file to: {file_path}")
            file.save(file_path)
            
            # Verify file was saved successfully
            if os.path.exists(file_path):
                print(f"File saved successfully: {filename}")
                return filename
            else:
                print("Error: File was not saved successfully")
                return None
        return None
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None
