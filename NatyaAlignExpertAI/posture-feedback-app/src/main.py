from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from video_upload import upload_video
from posture_analysis import analyze_posture
from feedback_generator import get_feedback

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    print("/upload endpoint was hit")
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded video
    video_path = upload_video(video_file)

    # Analyze the posture in the uploaded video
    analysis_results = analyze_posture(video_path)

    # Generate feedback and annotated video
    from feedback_generator import FeedbackGenerator
    model_path = '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl'
    generator = FeedbackGenerator(model_path)
    feedback = generator.analyze_posture(video_path)
    annotated_video_path = video_path.replace('.mp4', '_annotated.mp4')
    generator.annotate_video_with_feedback(video_path, annotated_video_path)

    return jsonify({
        'feedback': feedback,
        'annotated_video': annotated_video_path
    }), 200


# Serve the upload_test.html from root
@app.route('/')
def serve_upload_form():
    return send_from_directory('/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app', 'upload_test.html')

if __name__ == '__main__':
    app.run(debug=True)

# Serve uploaded files
from flask import send_from_directory

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)