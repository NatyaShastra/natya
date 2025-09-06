from cv2 import VideoCapture
import mediapipe as mp
import cv2
import pickle
import numpy as np

class PostureAnalyzer:
    def __init__(self, model_path):
        self.model_data = self.load_model(model_path)
        if len(self.model_data) == 3:
            self.model, self.label_encoder, self.step_map = self.model_data
            self.id_to_step = {v: k for k, v in self.step_map.items()} if self.step_map else {}
        else:
            self.model, self.label_encoder = self.model_data
            self.step_map = None
            self.id_to_step = {}
            
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
    
    def load_model(self, model_path):
        with open(model_path, 'rb') as model_file:
            return pickle.load(model_file)

    def analyze_video(self, video_path):
        cap = VideoCapture(video_path)
        frames_landmarks = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = self.extract_posture_data(results.pose_landmarks)
                flat_landmarks = self.flatten_landmarks(landmarks)
                frames_landmarks.append(flat_landmarks)

        cap.release()
        
        if not frames_landmarks:
            return ["No pose detected in video"]
            
        # Convert to numpy array
        landmarks_array = np.array(frames_landmarks)
        
        # First identify the dance step if we have step_map
        if self.step_map:
            identified_step, confidence = self.identify_dance_step(landmarks_array)
            
            # Then validate the posture
            feedback = self.validate_posture(landmarks_array, identified_step)
            
            # Add the step identification to the feedback
            feedback.insert(0, f"Identified dance step: {identified_step} (confidence: {confidence:.2f})")
            
            return feedback
        else:
            # Use the legacy comparison approach
            return self.legacy_analyze(landmarks_array)

    def extract_posture_data(self, landmarks):
        posture_data = []
        for landmark in landmarks.landmark:
            posture_data.append((landmark.x, landmark.y, landmark.z))
        return np.array(posture_data)
        
    def flatten_landmarks(self, landmarks):
        return landmarks.flatten()
        
    def identify_dance_step(self, landmarks_array):
        """First stage: Identify which dance step the student is performing"""
        # Extract features similar to training (mean and std of landmarks)
        T = landmarks_array.shape[0]
        flat = landmarks_array.reshape(T, -1)
        feat = np.concatenate([np.nanmean(flat, axis=0), np.nanstd(flat, axis=0)])
        
        # Get all possible step_ids
        step_ids = list(self.step_map.values())
        
        # Create test features for each possible step_id
        step_predictions = []
        for step_id in step_ids:
            # Create a copy of features for each possible step_id
            test_feat = np.hstack([feat, np.array([step_id], dtype=np.float32).reshape(-1, 1)])
            
            # Get probability of "correct" classification for this step_id
            probs = self.model.predict_proba(test_feat)
            
            # Find probability for "correct" class if it exists
            if "correct" in self.model.classes_:
                correct_idx = np.where(self.model.classes_ == "correct")[0][0]
                correct_prob = probs[0][correct_idx]
            else:
                # If no "correct" class, use the highest probability class
                correct_prob = probs.max()
                
            step_predictions.append((step_id, correct_prob))
        
        # Choose step_id with highest probability of being "correct"
        best_step_id, best_prob = max(step_predictions, key=lambda x: x[1])
        return self.id_to_step.get(best_step_id, "unknown"), best_prob

    def validate_posture(self, landmarks_array, step_id):
        """Second stage: Validate the posture for the identified step"""
        T = landmarks_array.shape[0]
        flat = landmarks_array.reshape(T, -1)
        feat = np.concatenate([np.nanmean(flat, axis=0), np.nanstd(flat, axis=0)])
        
        # Add the step_id feature
        step_id_num = self.step_map.get(step_id, 0)
        test_feat = np.hstack([feat, np.array([step_id_num], dtype=np.float32).reshape(-1, 1)])
        
        # Predict posture quality
        prediction = self.model.predict(test_feat)
        
        if self.label_encoder:
            correction_tip = self.label_encoder.inverse_transform(prediction)[0]
        else:
            correction_tip = prediction[0]
            
        return [correction_tip]
        
    def legacy_analyze(self, landmarks_array):
        """Legacy analysis for old model format"""
        results = []
        for landmarks in landmarks_array:
            prediction = self.model.predict([landmarks])
            if self.label_encoder:
                correction_tip = self.label_encoder.inverse_transform(prediction)[0]
            else:
                correction_tip = prediction[0]
            results.append(correction_tip)
        return results

    def compare_with_model(self, posture_data):
        # Legacy comparison logic, maintain for backward compatibility
        flattened = posture_data.flatten()
        prediction = self.model.predict([flattened])
        if self.label_encoder:
            return self.label_encoder.inverse_transform(prediction)[0]
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