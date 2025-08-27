#!/usr/bin/env python3
"""
Render 2D skeleton frames from landmarks with synthetic camera yaw to simulate multi-angle views.
This does not change the 3D pose but rotates x around z-axis as a proxy for yaw.
For more accurate multi-view, use 3D pose estimation + true camera transforms.
"""
import os
import glob
import numpy as np
import argparse
import cv2

# MediaPipe Pose connections (subset for clarity)
POSE_EDGES = [
    (11, 13), (13, 15),  # left arm
    (12, 14), (14, 16),  # right arm
    (11, 12),            # shoulders
    (23, 24),            # hips
    (11, 23), (12, 24),  # torso
    (23, 25), (25, 27),  # left leg
    (24, 26), (26, 28),  # right leg
]

N_JOINTS = 33
N_DIMS = 3


def rotate_yaw_xy(x, yaw_rad):
    # simple 2D rotation in x-y plane to simulate yaw
    c, s = np.cos(yaw_rad), np.sin(yaw_rad)
    R = np.array([[c, -s], [s, c]], dtype=np.float32)
    xy = x.reshape(-1, N_DIMS)[:, :2]
    xy_rot = xy @ R.T
    out = x.reshape(-1, N_DIMS).copy()
    out[:, :2] = xy_rot
    return out.reshape(-1)


def draw_skeleton(frame, joints2d, color=(0, 255, 0)):
    h, w = frame.shape[:2]
    pts = (joints2d * np.array([w, h], dtype=np.float32)).astype(int)
    for a, b in POSE_EDGES:
        pa = pts[a]
        pb = pts[b]
        cv2.line(frame, tuple(pa), tuple(pb), color, 2)
    for p in pts:
        cv2.circle(frame, tuple(p), 3, (255, 0, 0), -1)
    return frame


def main(in_dir, out_dir, view_set):
    os.makedirs(out_dir, exist_ok=True)
    views = {
        'front': 0.0,
        'left': np.deg2rad(45),
        'right': np.deg2rad(-45),
        'back': np.deg2rad(180),
    }
    if view_set:
        views = {k: views[k] for k in view_set if k in views}

    for npz_path in glob.glob(os.path.join(in_dir, '**', '*.npz'), recursive=True):
        data = np.load(npz_path, allow_pickle=True)
        lms = data['landmarks']  # (T,33,3) or (T,99), normalized 0-1
        base = os.path.splitext(os.path.basename(npz_path))[0]

        T = lms.shape[0]
        # Output under same relative tree
        rel = os.path.relpath(npz_path, in_dir)
        rel_dir = os.path.dirname(rel)
        for view_name, yaw in views.items():
            h, w = 480, 360
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_subdir = os.path.join(out_dir, rel_dir)
            os.makedirs(out_subdir, exist_ok=True)
            out_path = os.path.join(out_subdir, f"{base}__view-{view_name}.mp4")
            writer = cv2.VideoWriter(out_path, fourcc, 24, (w, h))
            for t in range(T):
                vec = lms[t]
                vec_view = rotate_yaw_xy(vec, yaw)
                joints2d = vec_view.reshape(-1, N_DIMS)[:, :2]
                frame = np.ones((h, w, 3), dtype=np.uint8) * 255
                frame = draw_skeleton(frame, joints2d)
                writer.write(frame)
            writer.release()
            print(f"[view] {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dir', default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/poses')
    parser.add_argument('--out', dest='out_dir', default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/videos')
    parser.add_argument('--views', nargs='*', default=['front','left','right','back'])
    args = parser.parse_args()
    main(args.in_dir, args.out_dir, args.views)