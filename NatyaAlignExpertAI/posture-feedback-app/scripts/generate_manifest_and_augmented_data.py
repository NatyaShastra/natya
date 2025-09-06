import os
import cv2
import mediapipe as mp
import numpy as np
import json
from pathlib import Path

def extract_landmarks(video_path):
    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(str(video_path))
    landmarks = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            lm = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark])
            landmarks.append(lm)
    cap.release()
    if landmarks:
        return np.stack(landmarks)
    return None

def augment_landmarks(landmarks, aug_type):
    # Simple augmentation: simulate slouch, shaking, not stiff, no smile
    aug = landmarks.copy()
    if aug_type == "slouch":
        aug[..., 1] += 0.05  # Lower y for torso
    elif aug_type == "shaking":
        aug += np.random.normal(0, 0.01, aug.shape)
    elif aug_type == "not_stiff":
        aug[..., 0] += np.random.normal(0, 0.02, aug[..., 0].shape)
    elif aug_type == "no_smile":
        # For now, just label, as smile needs face landmarks
        pass
    return aug

def main():
    raw_dir = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/raw_videos")
    out_dir = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/augmented")
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/manifests/train_strict.jsonl")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    aug_types = ["correct", "slouch", "shaking", "not_stiff", "no_smile"]
    with open(manifest_path, "w") as mf:
        for video_file in raw_dir.glob("*.mp4"):
            print(f"Processing {video_file}")
            lms = extract_landmarks(video_file)
            if lms is None:
                print(f"No landmarks found for {video_file}")
                continue
            for aug_type in aug_types:
                if aug_type == "correct":
                    aug_lms = lms
                else:
                    aug_lms = augment_landmarks(lms, aug_type)
                npz_path = out_dir / f"{video_file.stem}_{aug_type}.npz"
                np.savez_compressed(npz_path, landmarks=aug_lms)
                label = aug_type if aug_type != "correct" else "good_posture"
                step_id = video_file.stem  # Use filename as step_id
                rec = {"npz": str(npz_path), "label": label, "step_id": step_id}
                mf.write(json.dumps(rec) + "\n")
    print(f"Manifest and augmented data generated at {manifest_path}")

if __name__ == "__main__":
    main()
