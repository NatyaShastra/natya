import os
from typing import List, Dict

import cv2

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.image import Image, ImageFormat


def _load_pose_landmarker():
    """Load the MediaPipe PoseLandmarker model from a .task file.

    The model file path is expected to be set in the environment variable
    `POSE_LANDMARKER_MODEL_PATH`. If not provided, this function will raise.
    """

    model_path = os.environ.get("POSE_LANDMARKER_MODEL_PATH")
    if not model_path or not os.path.exists(model_path):
        raise FileNotFoundError(
            "MediaPipe PoseLandmarker model not found. "
            "Set POSE_LANDMARKER_MODEL_PATH to a valid `.task` model file."
        )

    base_options = BaseOptions(model_asset_path=model_path)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.VisionTaskRunningMode.VIDEO,
        min_pose_detection_confidence=0.5,
        min_pose_landmark_confidence=0.5,
    )

    return vision.PoseLandmarker.create_from_options(options)


def extract_pose_sequence(video_path: str) -> List[Dict]:
    """Extract a sequence of pose landmarks from a video using MediaPipe Tasks.

    Returns a list of frames where each frame contains landmark coordinates.
    """

    pose_sequence: List[Dict] = []

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Unable to open video: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")

    landmarker = _load_pose_landmarker()

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)

        timestamp_ms = int(frame_index * 1000 / fps)
        result = landmarker.detect_for_video(mp_image, timestamp_ms=timestamp_ms)

        if result.pose_landmarks and len(result.pose_landmarks) > 0:
            landmarks = []
            for landmark in result.pose_landmarks[0].landmarks:
                landmarks.append(
                    {
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z,
                        "visibility": landmark.visibility,
                    }
                )
            pose_sequence.append({
                "landmarks": landmarks,
                "frame_index": frame_index,
            })

        frame_index += 1

    cap.release()
    return pose_sequence
