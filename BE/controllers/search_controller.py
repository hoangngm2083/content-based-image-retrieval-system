from flask import request, jsonify
from services.search_service import search_hybrid
from services.file_service import remove_file, upload_file

def search():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    file_path = None

    try:
        # Bước 1: Upload ảnh
        file_path = upload_file(file)

        # Bước 2: Tìm kiếm
        results = search_hybrid(file_path)
        
        return jsonify(results)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    finally:
        # Bước 3: Xóa file sau khi xử lý
        if file_path:
            try:
                remove_file(file_path)
            except Exception as cleanup_err:
                print(f"[WARN] Failed to delete uploaded file: {cleanup_err}")
