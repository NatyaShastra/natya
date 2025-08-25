from cv2 import VideoCapture
import mediapipe as mp
import cv2
import pickle
import numpy as np

class PostureAnalyzer:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
    
    def load_model(self, model_path):
        with open(model_path, 'rb') as model_file:
            return pickle.load(model_file)

    def analyze_video(self, video_path):
        cap = VideoCapture(video_path)
        feedback = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                posture_data = self.extract_posture_data(results.pose_landmarks)
                feedback.append(self.compare_with_model(posture_data))

            # Removed imshow and waitKey for server compatibility

        cap.release()
    # Removed destroyAllWindows for server compatibility
        return feedback

    def extract_posture_data(self, landmarks):
        posture_data = []
        for landmark in landmarks.landmark:
            posture_data.append((landmark.x, landmark.y, landmark.z))
        return np.array(posture_data)

    def compare_with_model(self, posture_data):
        # Implement comparison logic with the trained model
        # This is a placeholder for actual comparison logic
        return "Feedback based on comparison"

# Example usage:
# analyzer = PostureAnalyzer('trained_model/model.pkl')
# feedback = analyzer.analyze_video('path_to_uploaded_video.mp4')
# print(feedback)

# Top-level function for main.py
def analyze_posture(video_path):
    model_path = '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl'
    analyzer = PostureAnalyzer(model_path)
    return analyzer.analyze_video(video_path)