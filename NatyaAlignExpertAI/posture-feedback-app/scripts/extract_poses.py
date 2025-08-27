#!/usr/bin/env python3
"""
Extract MediaPipe pose landmarks from raw videos and save per-frame landmarks to NPZ files
with metadata: step_id, angle, label.

Input folder layout (required):
 datasets/raw_videos/<step_id>/<angle>/<label>/<video_file>.mp4
  - step_id: e.g., adavu_001 ... adavu_120 (any string ok)
  - angle: front|left|right|back (free-form allowed)
  - label: correct|incorrect-<rule>

Output:
 datasets/processed/poses/<step_id>/<angle>/<label>/<video_stem>.npz
 Each NPZ contains arrays:
  - landmarks: shape (N, 33, 3) in normalized coordinates (x,y,z)
  - visibility: shape (N, 33)
  - meta: dict with keys {step_id, angle, label, video_path, fps}

Usage:
  python scripts/extract_poses.py --root datasets/raw_videos --out datasets/processed/poses
"""

import argparse
import os
import sys
from pathlib import Path
import json
import cv2
import numpy as np
from mediapipe import solutions as mp


def iter_videos(root: Path):
    for video_path in root.rglob("*.mp4"):
        parts = video_path.relative_to(root).parts
        if len(parts) < 4:
            # Expect step_id/angle/label/file
            print(f"[skip] Unexpected path: {video_path}")
            continue
        step_id, angle, label = parts[0], parts[1], parts[2]
        yield step_id, angle, label, video_path


def extract_video(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    pose = mp.pose.Pose(static_image_mode=False,
                        model_complexity=2,
                        enable_segmentation=False,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    frames_landmarks = []
    frames_visibility = []

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)
            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark
                arr = np.array([[p.x, p.y, p.z] for p in lm], dtype=np.float32)
                vis = np.array([p.visibility for p in lm], dtype=np.float32)
            else:
                arr = np.full((33, 3), np.nan, dtype=np.float32)
                vis = np.zeros((33,), dtype=np.float32)
            frames_landmarks.append(arr)
            frames_visibility.append(vis)
    finally:
        cap.release()
        pose.close()

    landmarks = np.stack(frames_landmarks, axis=0) if frames_landmarks else np.empty((0,33,3), np.float32)
    visibility = np.stack(frames_visibility, axis=0) if frames_visibility else np.empty((0,33), np.float32)
    return landmarks, visibility, fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path('datasets/raw_videos'))
    ap.add_argument('--out', type=Path, default=Path('datasets/processed/poses'))
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    for step_id, angle, label, video_path in iter_videos(args.root):
        try:
            lms, vis, fps = extract_video(video_path)
        except Exception as e:
            print(f"[error] {video_path}: {e}")
            continue
        rel = video_path.relative_to(args.root)
        out_path = args.out / rel.with_suffix('.npz')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            'step_id': step_id,
            'angle': angle,
            'label': label,
            'video_path': str(video_path),
            'fps': fps,
        }
        np.savez_compressed(out_path, landmarks=lms, visibility=vis, meta=json.dumps(meta))
        print(f"[ok] {video_path} -> {out_path} ({lms.shape[0]} frames)")


if __name__ == '__main__':
    main()
