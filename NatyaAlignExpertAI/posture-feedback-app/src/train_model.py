import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
import os


# List of (video_path, correction) tuples
TRAINING_DATA = [
    ("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/uploads/student1.mp4", "Heel not placed flat"),
    ("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/uploads/student2.mp4", "Back is not straight, hand not placed properly"),
    ("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/uploads/student3.mp4", "Legs not raised, no Araimandi, body not tight, body shaking"),
    ("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/uploads/student4.mp4", "Bad body control, zero balance, hands not placed properly"),
]

X = []  # feature vectors
y = []  # correction labels

mp_pose = mp.solutions.pose.Pose()

for video_path, correction in TRAINING_DATA:
    if not os.path.exists(video_path):
        print(f"Warning: {video_path} not found, skipping.")
        continue
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
            X.append(landmarks)
            y.append(correction)
    cap.release()


if len(X) == 0:
    print("No training data found. Please check your video paths and labels.")
    exit(1)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

clf = RandomForestClassifier()
clf.fit(X, y_encoded)


os.makedirs("trained_model", exist_ok=True)
with open("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl", "wb") as f:
    pickle.dump((clf, le), f)

print("Model trained and saved to trained_model/model.pkl with correction tips.")
