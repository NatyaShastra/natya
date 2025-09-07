@app.route("/")
def index():
    return "NatyaAlignExpertAI backend is running!"
import threading
from google_drive_upload import upload_feedback_and_video
import os
from flask import Flask, request, jsonify, send_from_directory, send_file, current_app
from flask_cors import CORS
from video_upload import upload_video
from posture_analysis import analyze_posture
from feedback_generator import get_feedback, FeedbackGenerator
from dance_steps import get_available_dance_steps, get_step_id_from_name
from extend_video import process_all_videos_in_directory, ensure_min_duration
from ffmpeg_utils import cv2_frames_to_ffmpeg_video
from utils.video_utils import downscale_video

app = Flask(__name__)
CORS(app)

# Set absolute path to the uploads directory
UPLOAD_DIR = '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/uploads'

# Process existing videos on startup to ensure they meet minimum duration
# Use with_appcontext for newer Flask versions
def process_existing_videos():
    with app.app_context():
        process_all_videos_in_directory(UPLOAD_DIR, min_duration=10.0)

# Use a request handler to process videos on first request
first_request_processed = False
@app.before_request
def ensure_video_processing():
    global first_request_processed
    if not first_request_processed:
        process_existing_videos()
        first_request_processed = True

@app.route('/dance_steps', methods=['GET'])
def get_dance_steps():
    """Endpoint to get the list of available dance steps"""
    dance_steps = get_available_dance_steps()
    return jsonify(dance_steps)

@app.route('/upload', methods=['POST'])
def upload():
    print("/upload endpoint was hit")
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Get the selected dance step if provided
    selected_dance_step = request.form.get('danceStep', '')
    print(f"Selected dance step: {selected_dance_step}")

    # Save the uploaded video
    video_path = upload_video(video_file)
    
    # Optionally downscale the video for faster processing
    downscale_enabled = request.form.get('downscale', 'true').lower() == 'true'
    if downscale_enabled:
        # Get target width from request, default to 640px if not provided
        target_width = int(request.form.get('targetWidth', 640))
        print(f"Downscaling video to width: {target_width}px")
        
        # Create a temporary file for the downscaled video
        filename, ext = os.path.splitext(video_path)
        downscaled_path = f"{filename}_downscaled{ext}"
        
        # Downscale the video
        video_path = downscale_video(video_path, downscaled_path, target_width=target_width)


    # Get model selection from request (default to strict)
    selected_model = request.form.get('model', 'strict')
    if selected_model == 'strict':
        model_path = '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model_strict.pkl'
    else:
        model_path = '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model_generated.pkl'

    try:
        generator = FeedbackGenerator(model_path)
        # If user specified a dance step, use it for more accurate feedback
        if selected_dance_step:
            feedback = generator.analyze_posture_with_step(video_path, selected_dance_step)
        else:
            # Otherwise use automatic detection
            feedback = generator.analyze_posture(video_path)
    except Exception as e:
        print(f"Error generating feedback: {e}")
        feedback = ["Error analyzing video. Please try again."]

    # --- LLM User-Friendly Feedback Generation ---
    # Use the original feedback list as user-friendly feedback
    user_friendly_feedback = feedback
        
    # Get the filename from the full path
    video_filename = os.path.basename(video_path)
    annotated_video_filename = video_filename.replace('.mp4', '_annotated.mp4')
    
    # Full path for the annotated video
    full_annotated_path = os.path.join(UPLOAD_DIR, annotated_video_filename)
    
    print(f"Original video path: {video_path}")
    print(f"Annotated video filename: {annotated_video_filename}")
    print(f"Full annotated path: {full_annotated_path}")
    
    # Generate annotated video with multiple fallback mechanisms
    try:
        # Get frame sample rate from request, default to 3 if not provided
        # Higher values (5-10) = faster but lower quality, lower values (1-2) = slower but higher quality
        frame_sample_rate = int(request.form.get('frameSampleRate', 3))
        print(f"Using frame sample rate: {frame_sample_rate}")
        
        # Generate annotated video
        if selected_dance_step:
            result, detailed_feedback = generator.annotate_video_with_feedback(
                video_path, 
                full_annotated_path, 
                specified_step=selected_dance_step,
                frame_sample_rate=frame_sample_rate
            )
        else:
            result, detailed_feedback = generator.annotate_video_with_feedback(
                video_path, 
                full_annotated_path,
                frame_sample_rate=frame_sample_rate
            )
        
        # Merge the detailed feedback with the original feedback
        if detailed_feedback:
            feedback.extend(detailed_feedback)
        
        # Check if video generation was successful
        if result is None or not os.path.exists(full_annotated_path) or os.path.getsize(full_annotated_path) == 0:
            print(f"Failed to generate annotated video with primary method: {full_annotated_path}")
            print("Attempting to use ffmpeg fallback for video creation...")
            
            # Try to analyze posture with ffmpeg directly
            import cv2
            cap = cv2.VideoCapture(video_path)
            frames = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            
            cap.release()
            
            if frames:
                # Add feedback text to last frame
                feedback_frame = frames[-1].copy()
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (0, 0, 255)  # Red color for feedback
                
                # Add feedback text
                y = 50
                for line in feedback:
                    cv2.putText(feedback_frame, line, (30, y), font, 0.7, color, 2)
                    y += 30
                
                # Add feedback frame for 3 seconds at end
                fps = 30
                for _ in range(fps * 3):
                    frames.append(feedback_frame)
                
                # Use ffmpeg to create the video
                if cv2_frames_to_ffmpeg_video(frames, full_annotated_path, fps):
                    print(f"Successfully created video with ffmpeg fallback: {full_annotated_path}")
                    result = full_annotated_path
                else:
                    print(f"Failed to create video with ffmpeg fallback: {full_annotated_path}")
                    # Return only feedback without annotated video
                    return jsonify({
                        'feedback': feedback,
                        'error': 'Could not generate annotated video',
                        'original_video': f'/raw_video/{os.path.basename(video_path)}'
                    }), 500
    except Exception as e:
        print(f"Error generating annotated video: {e}")
        # Return only feedback without annotated video
        return jsonify({
            'feedback': feedback,
            'error': f'Exception while generating annotated video: {str(e)}',
            'original_video': f'/raw_video/{os.path.basename(video_path)}'
        }), 500
    
    # Ensure the annotated video meets minimum duration
    try:
        ensure_min_duration(full_annotated_path, min_duration=10.0)
    except Exception as e:
        print(f"Error extending video duration: {e}")
        # Continue anyway, as we at least have the video
    

    # --- Google Drive Integration ---
    # Extract all needed data before starting thread
    student_id = request.form.get('student_id', video_filename.split('.')[0])
    feedback_text = '\n'.join(user_friendly_feedback if isinstance(user_friendly_feedback, list) else [str(user_friendly_feedback)])
    final_video_path = full_annotated_path

    def drive_upload_task(student_id, feedback_text, final_video_path):
        try:
            print(f"[Drive] Starting upload for student: {student_id}")
            print(f"[Drive] Feedback text: {feedback_text[:100]}... (truncated)")
            print(f"[Drive] Video path: {final_video_path}")
            upload_feedback_and_video(feedback_text, final_video_path, student_id)
            print(f"[Drive] Upload to Google Drive complete for student: {student_id}")
        except Exception as e:
            print(f"[Drive] Error uploading to Google Drive: {e}")

    threading.Thread(target=drive_upload_task, args=(student_id, feedback_text, final_video_path), daemon=True).start()

    # Return direct file path for client
    return jsonify({
        'feedback': feedback,  # Original feedback list
        'user_friendly_feedback': user_friendly_feedback,  # LLM-generated user-friendly feedback
        'annotated_video': f'/raw_video/{annotated_video_filename}'
    }), 200


# Serve the upload_test.html from root
@app.route('/')
def serve_upload_form():
    return send_from_directory('/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app', 'upload_test.html')

# Add a test page for video playback
@app.route('/test_video')
def serve_test_video():
    return send_from_directory('/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app', 'test_video.html')

# Direct file access with improved video streaming
@app.route('/raw_video/<path:filename>')
def raw_video(filename):
    video_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(video_path):
        print(f"Serving video file: {video_path}")
        
        # Get file size for Content-Length header
        file_size = os.path.getsize(video_path)
        
        # Set caching headers to improve performance
        response = send_file(
            video_path,
            mimetype='video/mp4',
            as_attachment=False,
            download_name=filename,
            conditional=True  # Support for If-Modified-Since header
        )
        
        # Add additional headers for better video streaming
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
        response.headers['Content-Length'] = file_size
        
        return response
    else:
        print(f"Video file not found: {video_path}")
        return "Video not found", 404

# Legacy routes for backward compatibility
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    print(f"Legacy route called for: {filename}")
    return send_from_directory(UPLOAD_DIR, filename)

@app.route('/video/<path:filename>')
def direct_video(filename):
    print(f"Alternative route called for: {filename}")
    return send_from_directory(UPLOAD_DIR, filename, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)