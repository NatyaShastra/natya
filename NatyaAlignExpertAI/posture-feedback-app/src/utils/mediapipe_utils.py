import cv2
import mediapipe as mp

def initialize_mediapipe_pose():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    return pose

def process_video_frame(frame, pose):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        return results.pose_landmarks
    else:
        return None

def draw_landmarks(frame, landmarks):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(frame, landmarks, mp.solutions.pose.POSE_CONNECTIONS)

def release_resources(pose):
    pose.close()