import os
import glob
import json
import argparse
import numpy as np

"""
Build a JSONL manifest combining .npz pose files with metadata for training.
Each line: {"npz": "/path/file.npz", "step_id": str, "angle": str, "label": str}
"""

def main(in_dirs, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        for in_dir in in_dirs:
            for npz_path in glob.glob(os.path.join(in_dir, '**', '*.npz'), recursive=True):
                data = np.load(npz_path, allow_pickle=True)
                if 'meta' in data:
                    meta = json.loads(str(data['meta']))
                    step_id = meta.get('step_id', 'unknown')
                    angle = meta.get('angle', 'unknown')
                    label = meta.get('label', 'unknown')
                else:
                    step_id = str(data['step_id']) if 'step_id' in data else 'unknown'
                    angle = str(data['angle']) if 'angle' in data else 'unknown'
                    label = str(data['label']) if 'label' in data else 'unknown'
                rec = {"npz": npz_path, "step_id": step_id, "angle": angle, "label": label}
                f.write(json.dumps(rec) + "\n")
                print(f"[manifest] {npz_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dirs', nargs='+', default=[
        '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/poses',
        '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/processed/poses_aug',
    ])
    parser.add_argument('--out', dest='out_path', default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/manifests/train.jsonl')
    args = parser.parse_args()
    main(args.in_dirs, args.out_path)
