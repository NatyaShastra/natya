import os
import glob
import numpy as np
import argparse
import json
from pathlib import Path

"""
Generate incorrect pose samples by perturbing correct pose .npz files.
Supports NPZ saved with either separate fields (step_id, angle, label) or a 'meta' JSON string.

Input (recommended): datasets/processed/poses/<step>/<angle>/correct/*.npz
Output: datasets/processed/poses_aug/<step>/<angle>/incorrect-<rule>/*.npz
"""

# indices for major joints in MediaPipe Pose (33 joints)
HEAD_IDX = [0]
SHOULDER_IDX = [11, 12]
ELBOW_IDX = [13, 14]
WRIST_IDX = [15, 16]
HIP_IDX = [23, 24]
KNEE_IDX = [25, 26]
ANKLE_IDX = [27, 28]

N_DIMS = 3


def _slouch(flat: np.ndarray):
    # shoulders: y down, z forward
    idx = np.array(SHOULDER_IDX) * N_DIMS
    flat[:, idx + 1] += 0.03
    flat[:, idx + 2] += 0.05
    return flat


def _knees_in(flat: np.ndarray):
    left_knee = KNEE_IDX[0] * N_DIMS
    right_knee = KNEE_IDX[1] * N_DIMS
    flat[:, left_knee + 0] += 0.02
    flat[:, right_knee + 0] -= 0.02
    return flat


def _arms_low(flat: np.ndarray):
    for idx in ELBOW_IDX + WRIST_IDX:
        base = idx * N_DIMS
        flat[:, base + 1] += 0.05
    return flat


def _feet_misaligned(flat: np.ndarray):
    flat[:, ANKLE_IDX[0] * N_DIMS + 0] += 0.03
    flat[:, ANKLE_IDX[1] * N_DIMS + 0] -= 0.03
    return flat


AUGS = {
    'slouch': _slouch,
    'knees_in': _knees_in,
    'arms_low': _arms_low,
    'feet_misaligned': _feet_misaligned,
}


def to_flat(lms: np.ndarray) -> np.ndarray:
    # Accept (T,33,3) or (T, 99)
    if lms.ndim == 3:
        T = lms.shape[0]
        return lms.reshape(T, -1)
    return lms


def to_shaped(flat: np.ndarray, ref_shape: tuple) -> np.ndarray:
    if len(ref_shape) == 3:
        T = flat.shape[0]
        return flat.reshape(T, ref_shape[1], ref_shape[2])
    return flat


def load_npz(path: Path):
    data = np.load(path, allow_pickle=True)
    lms = data['landmarks']
    vis = data['visibility'] if 'visibility' in data else None
    if 'meta' in data:
        meta = json.loads(str(data['meta']))
        step_id = meta.get('step_id', 'unknown')
        angle = meta.get('angle', 'unknown')
        label = meta.get('label', 'unknown')
    else:
        step_id = str(data['step_id']) if 'step_id' in data else 'unknown'
        angle = str(data['angle']) if 'angle' in data else 'unknown'
        label = str(data['label']) if 'label' in data else 'unknown'
    return lms, vis, {'step_id': step_id, 'angle': angle, 'label': label}


def save_npz(path: Path, lms: np.ndarray, vis, meta: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, landmarks=lms, visibility=(vis if vis is not None else np.array([])), meta=json.dumps(meta))


def main(in_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for npz_path in glob.glob(os.path.join(in_dir, '**', 'correct', '*.npz'), recursive=True):
        lms, vis, meta = load_npz(Path(npz_path))
        if meta.get('label') != 'correct':
            # Enforce using only correct inputs as seeds
            continue
        ref_shape = lms.shape
        flat = to_flat(lms).copy()
        for aug_name, fn in AUGS.items():
            aug_flat = fn(flat.copy())
            aug_lms = to_shaped(aug_flat, ref_shape)
            new_meta = dict(meta)
            new_meta['label'] = f'incorrect-{aug_name}'
            # path: <step>/<angle>/incorrect-aug/<file>
            rel = Path(npz_path).relative_to(in_dir)
            out_rel = Path(*rel.parts[:-2]) / rel.parts[-2] / f"incorrect-{aug_name}" / rel.name
            out_path = Path(out_dir) / out_rel
            save_npz(out_path, aug_lms, vis, new_meta)
            print(f"[aug] {rel} -> {out_rel}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dir', default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/poses')
    parser.add_argument('--out', dest='out_dir', default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/poses_aug')
    args = parser.parse_args()
    main(args.in_dir, args.out_dir)
