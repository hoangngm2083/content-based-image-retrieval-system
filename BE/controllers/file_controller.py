from flask import Response,request,jsonify
import traceback
from services.file_service import upload_file as upload_file_service
from services.feature_extractor_service import extract_color_layout, extract_vgg_feature
from services.database_service import insert_image
from services.file_service import remove_file
import os
from werkzeug.exceptions import BadRequest, InternalServerError

from services.file_service import extract_zip, upload_file_from_path
from services.file_service import clear_temp
from services.file_service import clear_zip


def upload_file():
    """
    Handle image upload, extract features, and save them to the database.

    Returns:
        JSON response with file path if successful, or an error message.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    file_path = None
    try:
        # Upload and save the image
        file_path = upload_file_service(file)

        # Feature extraction
        color_layout = extract_color_layout(file_path)
        vgg_features = extract_vgg_feature(file_path).tolist()

        # Save to database
        insert_image(file_path, color_layout, vgg_features)

        return jsonify({'message': 'File uploaded and processed successfully', 'path': file_path}), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        if file_path:
            try:
                print("***** remove file")
                remove_file(file_path)
            except Exception as cleanup_err:
                print(f"[WARN] Failed to delete uploaded file: {cleanup_err}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


def upload_files()-> Response:
    """
    Handle multiple image uploads, validate, and save them to the upload folder.

    Returns:
        JSON response with a list of uploaded filenames if successful, or an error message.

    Raises:
        BadRequest: If the number of files exceeds 5 or a file is invalid.
        InternalServerError: If there is an error saving a file or an unexpected error occurs.
    """
    try:
        # Get list of files from request
        files = request.files.getlist("images")
        
        # Check the number of files
        if len(files) > 5:
            raise BadRequest("Maximum of 5 images allowed")

        # List to store uploaded filenames
        filenames = []
        
        # Process each file
        for file in files:
            # Check if the file is valid and has a supported format
            if file and file.filename and file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = None
                try:
                     # Upload and save the image
                    file_path = upload_file_service(file)

                     # Add filename to the list
                    filenames.append(file.filename)

                    # Feature extraction
                    color_layout = extract_color_layout(file_path)
                    vgg_features = extract_vgg_feature(file_path).tolist()

                    # Save to database
                    insert_image(file_path, color_layout, vgg_features)
                
                except Exception as e:

                    if file_path:
                        remove_file(file_path)
                    # Handle other unknown errors during file saving
                    raise InternalServerError(f"Unexpected error while processing file {file.filename}: {str(e)}")
            else:
                # Invalid file or unsupported format
                raise BadRequest(f"Invalid or unsupported file format: {file.filename}")

        # Return list of uploaded files
        return jsonify({"uploaded": filenames}), 200

    except Exception as e:
        # General error handling
        # Convert traceback to string
        tb_str = "".join(traceback.format_tb(e.__traceback__))
        return jsonify({
            "error": str(e),
            "tracking": tb_str
        }), 500


def upload_zip():
    try:
        file = request.files.get("file")
        if not file or not file.filename.endswith(".zip"):
            raise ValueError("File không hợp lệ")

        
        extracted_dir=extract_zip(file)
    


        if not os.path.isdir(extracted_dir):
            raise ValueError('Đường dẫn không phải là một folder hợp lệ')

        # Khởi tạo kết quả
        results = {'success': 0, 'errors': []}

        # Lặp qua từng file trong folder
        for filename in os.listdir(extracted_dir):
            if ".jpg" not in filename:
                continue

  
            file_path = os.path.join(extracted_dir, filename)
            if os.path.isfile(file_path):  # Chỉ xử lý các file, không xử lý thư mục con
                try:
                    # Upload và lưu ảnh
                    uploaded_path = upload_file_from_path(file_path)

                    # Trích xuất đặc trưng
                    color_layout = extract_color_layout(uploaded_path)
                    vgg_features = extract_vgg_feature(uploaded_path).tolist()

                    # Lưu vào cơ sở dữ liệu
                    insert_image(uploaded_path, color_layout, vgg_features)

                    # Tăng số lượng ảnh xử lý thành công
                    results['success'] += 1

                except ValueError as ve:
                    # Ghi nhận lỗi liên quan đến giá trị không hợp lệ
                    results['errors'].append({'file': filename, 'error': str(ve)})
                except Exception as e:
                    # Xử lý lỗi server nội bộ và dọn dẹp file đã upload (nếu có)
                    if 'uploaded_path' in locals():
                        try:
                            remove_file(uploaded_path)
                        except Exception as cleanup_err:
                            print(f"[WARN] Không thể xóa file đã upload: {cleanup_err}")
                    results['errors'].append({
                        'file': filename,
                        'error': 'Lỗi server nội bộ',
                        'details': str(e)
                    })


       
        # Trả về kết quả
        if results['errors']:
            raise ValueError("Có lỗi xảy ra trong quá trình upload nhiều ảnh")  # 207 Multi-Status nếu có lỗi
        else:
            return jsonify(results), 200  # 200 OK nếu tất cả thành công

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        clear_temp()
        clear_zip()

       

