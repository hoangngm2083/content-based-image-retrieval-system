
import os

def config(app):
    app.config['UPLOAD_FOLDER'] = os.getenv('APP_UPLOAD_FOLDER', 'static/images/')
    app.config['ZIP_FOLDER'] = os.getenv('APP_ZIP_FOLDER', 'static/zips/')
    app.config['TEMP_IMG_FOLDER'] = os.getenv('APP_TEMP_IMG_FOLDER', 'static/temps/')

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['ZIP_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_IMG_FOLDER'], exist_ok=True)

    # Các biến môi trường dùng cho database
    app.config['DB_HOST'] = os.getenv('DB_HOST', 'localhost')
    app.config['DB_NAME'] = os.getenv('DB_NAME', 'mydatabase')
    app.config['DB_USER'] = os.getenv('DB_USER', 'myuser')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', 'mypassword')