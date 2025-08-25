from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video(video_file):
    # Save the uploaded file to disk and return the path
    if allowed_file(video_file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(filepath)
        return filepath
    else:
        raise ValueError('File type not allowed')

if __name__ == '__main__':
    app.run(debug=True)