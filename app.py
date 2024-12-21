from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the directory for uploads relative to this file
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the route for index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Initialize upload route
@app.route('/uploads', methods=['POST'])
def upload_img():
    category = request.form.get('category')
    if not category:
        return jsonify({"error": "Category is required"}), 400

    # Create the category folder if it doesn't exist
    category_folder = os.path.join(app.config['UPLOAD_FOLDER'], category)
    os.makedirs(category_folder, exist_ok=True)

    # Get the uploaded files
    upload_files = request.files.getlist('images')
    if not upload_files:
        return jsonify({"error": "No files uploaded"}), 400

    # Save files to the category folder
    saved_files = []  # Correct variable name here
    for file in upload_files:
        # Secure the filename to prevent any malicious filenames
        filename = secure_filename(file.filename)
        file_path = os.path.join(category_folder, filename)
        
        # Save the file
        file.save(file_path)
        saved_files.append(filename)

    return jsonify({"message": "Files uploaded successfully", "files": saved_files}), 200

if __name__ == '__main__':
    app.run(debug=True)
