from mediapipe import solutions as mp
import cv2
import numpy as np
import pickle

class FeedbackGenerator:
    def annotate_video_with_feedback(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        all_feedbacks = []
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            correction_tip = "No pose detected"
            if results.pose_landmarks:
                landmarks = self._extract_landmarks(results.pose_landmarks)
                prediction = self.model.predict([landmarks])
                correction_tip = self.label_encoder.inverse_transform(prediction)[0]
                mp_drawing = mp.drawing_utils
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp.pose.POSE_CONNECTIONS)
            all_feedbacks.append(correction_tip)
            frames.append(frame)

        cap.release()

        # Find top 3 most frequent actionable corrections
        from collections import Counter
        feedback_counts = Counter(all_feedbacks)
        # Only actionable corrections (negative feedback)
        def is_correction(fb):
            fb_lower = fb.lower()
            return (
                "not" in fb_lower or "imperfect" in fb_lower or "bad" in fb_lower or "incorrect" in fb_lower or "zero" in fb_lower or "shaking" in fb_lower or "wrong" in fb_lower
            )
        corrections = [fb for fb, _ in feedback_counts.most_common() if is_correction(fb)]
        top_corrections = corrections[:3]

        # Write all original frames first
        for frame in frames:
            out.write(frame)

        # Create a final feedback frame with a simple statement
        feedback_frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # white background
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        color = (0, 0, 0)
        y0 = height // 2 - 40
        import textwrap
        max_width_px = width - 60
        char_width_px = 7  # More conservative estimate for wrapping
        max_chars = max_width_px // char_width_px
        if top_corrections:
            summary_statement = "Please correct the following: " + ", ".join(top_corrections) + "."
        else:
            summary_statement = "No major corrections detected."
        wrapped_lines = textwrap.wrap(summary_statement, width=max_chars)
        for i, line in enumerate(wrapped_lines):
            cv2.putText(feedback_frame, line, (30, y0 + i * 35), font, font_scale, color, 2, cv2.LINE_AA)

        # Show feedback frame for 3 seconds (or as many frames as needed)
        for _ in range(fps * 3):
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