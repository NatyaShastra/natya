from mediapipe import solutions as mp
import cv2
import numpy as np
import pickle

class FeedbackGenerator:
    def annotate_video_with_feedback(self, student_video_path, reference_video_path, output_path):
        cap_student = cv2.VideoCapture(student_video_path)
        cap_ref = cv2.VideoCapture(reference_video_path)
        # Use a widely supported codec and ensure consistent frame size
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4v is widely supported
        fps = int(cap_student.get(cv2.CAP_PROP_FPS))
        width = int(cap_student.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap_student.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ref_width = int(width * 2)  # Increase reference video width by 50%
        target_size = (width, height)
        ref_size = (ref_width, height)
        out_width = width + ref_width
        out_height = height
        out = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))

        all_feedbacks = []
        frames = []
        # Get frame counts for both videos
        student_frame_count = int(cap_student.get(cv2.CAP_PROP_FRAME_COUNT))
        ref_frame_count = int(cap_ref.get(cv2.CAP_PROP_FRAME_COUNT))
        max_frames = max(student_frame_count, ref_frame_count, int(fps * 7))

        last_frame_s = None
        last_frame_r = None
        for i in range(max_frames):
            ret_s, frame_s = cap_student.read()
            ret_r, frame_r = cap_ref.read()
            if ret_s:
                frame_s = cv2.resize(frame_s, target_size)
                last_frame_s = frame_s.copy()
            else:
                frame_s = last_frame_s if last_frame_s is not None else np.zeros((height, width, 3), dtype=np.uint8)
            if ret_r:
                frame_r = cv2.resize(frame_r, ref_size)
                last_frame_r = frame_r.copy()
            else:
                frame_r = last_frame_r if last_frame_r is not None else np.zeros((height, ref_width, 3), dtype=np.uint8)
            # Annotate student frame
            results = self.mp_pose.process(cv2.cvtColor(frame_s, cv2.COLOR_BGR2RGB))
            correction_tip = "No pose detected"
            if results.pose_landmarks:
                landmarks = self._extract_landmarks(results.pose_landmarks)
                prediction = self.model.predict([landmarks])
                correction_tip = self.label_encoder.inverse_transform(prediction)[0]
                mp_drawing = mp.drawing_utils
                mp_drawing.draw_landmarks(frame_s, results.pose_landmarks, mp.pose.POSE_CONNECTIONS)
            all_feedbacks.append(correction_tip)
            # Concatenate reference and student frames side by side
            combined_frame = np.hstack((frame_r, frame_s))
            frames.append(combined_frame)

        cap_student.release()
        cap_ref.release()

        # Find top 3 most frequent actionable corrections
        from collections import Counter
        feedback_counts = Counter(all_feedbacks)
        def is_correction(fb):
            fb_lower = fb.lower()
            return (
                "not" in fb_lower or "imperfect" in fb_lower or "bad" in fb_lower or "incorrect" in fb_lower or "zero" in fb_lower or "shaking" in fb_lower or "wrong" in fb_lower
            )
        corrections = [fb for fb, _ in feedback_counts.most_common() if is_correction(fb)]
        top_corrections = corrections[:3]

        # Ensure playback for full video length or minimum 7 seconds, whichever is higher
        min_frames = int(fps * 7)
        if len(frames) < min_frames:
            # Repeat frames only if video is shorter than 7 seconds
            repeat_count = (min_frames + len(frames) - 1) // len(frames)
            frames = frames * repeat_count
            frames = frames[:min_frames]
        # Write all combined frames (no repetition if video is longer than 7 seconds)
        for frame in frames:
            out.write(frame)

        # Create a final feedback frame with a simple statement
        feedback_frame = np.ones((out_height, out_width, 3), dtype=np.uint8) * 255  # white background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        color = (0, 0, 0)
        y0 = out_height // 2 - 40
        import textwrap
        max_width_px = out_width - 60
        char_width_px = 7
        max_chars = max_width_px // char_width_px
        if top_corrections:
            summary_statement = "Please correct the following: " + ", ".join(top_corrections) + "."
        else:
            summary_statement = "No major corrections detected."
        wrapped_lines = textwrap.wrap(summary_statement, width=max_chars)
        for i, line in enumerate(wrapped_lines):
            cv2.putText(feedback_frame, line, (30, y0 + i * 35), font, font_scale, color, 2, cv2.LINE_AA)

        # Show feedback frame for 7 seconds (or as many frames as needed)
        for _ in range(fps * 7):
            out.write(feedback_frame)

        # Keep the video open and ON by repeating the last feedback frame for additional 7 seconds
        for _ in range(fps * 7):
            out.write(feedback_frame)

        out.release()
        return output_path
    def __init__(self, model_path):
        with open(model_path, 'rb') as model_file:
            self.model, self.label_encoder = pickle.load(model_file)
        self.mp_pose = mp.pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def analyze_posture(self, video_path):
        cap = cv2.VideoCapture(video_path)
        feedback = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process the frame with MediaPipe
            results = self.mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                landmarks = self._extract_landmarks(results.pose_landmarks)
                prediction = self.model.predict([landmarks])
                correction_tip = self.label_encoder.inverse_transform(prediction)[0]
                feedback.append(correction_tip)

        cap.release()
        return feedback

    def _extract_landmarks(self, landmarks):
        return np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark]).flatten()

    # No longer needed, feedback is now the correction tip from the model

def get_feedback(video_path):
    generator = FeedbackGenerator('/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl')
    return generator.analyze_posture(video_path)