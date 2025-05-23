from flask import current_app

import os
import uuid
import zipfile
import shutil


def upload_file(file):
    """
    Save the uploaded image file to the configured upload folder.

    Args:
        file: File object from request.files

    Returns:
        file_path: The full path to the saved file

    Raises:
        ValueError: If the filename is empty
        Exception: If an error occurs while saving the file
    """
    if not file or file.filename.strip() == '':
        raise ValueError('Empty filename')

    uuid_str = str(uuid.uuid4())
    _, ext = os.path.splitext(file.filename)
    ext = ext if ext else '.jpg'
    filename = f"{uuid_str}{ext}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return file_path


def remove_file(file_path):
    """
    Delete the specified file from the filesystem.

    Args:
        file_path: Path to the file to be deleted

    Raises:
        Exception: If an error occurs during deletion
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as cleanup_err:
        print(f"[WARN] Failed to delete uploaded file: {cleanup_err}")
        raise cleanup_err


def upload_file_from_path(file_path):
    filename  = str(uuid.uuid4())+'.jpg'

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    dest_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    shutil.copy(file_path, dest_path)
    return dest_path


def extract_zip(file):
    zip_folder = current_app.config['ZIP_FOLDER']
    os.makedirs(zip_folder, exist_ok=True)

    # Tạo đường dẫn tới file zip
    zip_path = os.path.join(zip_folder, f"{uuid.uuid4()}.zip")
    file.save(zip_path)

    # Tạo thư mục để giải nén
    extracted_dir = current_app.config['TEMP_IMG_FOLDER']


    os.makedirs(extracted_dir, exist_ok=True)

    # Giải nén file vào thư mục
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)

    return extracted_dir
def clear_temp():
     # Tạo thư mục để giải nén
    extracted_dir = current_app.config['TEMP_IMG_FOLDER']

    shutil.rmtree(extracted_dir)

def clear_zip():
     # Tạo thư mục để giải nén
    extracted_dir = current_app.config['ZIP_FOLDER']

    shutil.rmtree(extracted_dir)