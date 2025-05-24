from flask import Flask, jsonify,Response

from configs import config
from flask_cors import CORS

from controllers.file_controller import upload_file,upload_zip, upload_files
from controllers.search_controller import search


app = Flask(__name__)
config(app)  # Load config from function
CORS(app)


@app.route('/')
def home():
    return "Flask app with Docker and PostgreSQL!"

@app.route('/upload', methods=['POST'])
def upload_route():
    try:
        return upload_file()
        # return "reload"
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  


@app.route("/upload_images", methods=["POST"])
def upload_images_route() -> Response:
    return upload_files()

@app.route("/upload_zip", methods=["POST"])
def upload_zip_route()-> Response:
  return upload_zip()

@app.route("/search", methods=["POST"])
def search_route():
    try:
        return search()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)
