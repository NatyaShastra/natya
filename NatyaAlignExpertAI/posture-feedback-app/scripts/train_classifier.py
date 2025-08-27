#!/usr/bin/env python3
"""
Train a classifier that predicts feedback labels using pose landmarks and step_id as input features.
Reads a JSONL manifest created by scripts/build_manifest.py.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def load_samples(manifest_path: Path):
    X = []
    y = []
    step_ids = []
    with open(manifest_path, 'r') as f:
        for line in f:
            rec = json.loads(line)
            npz = np.load(rec['npz'], allow_pickle=True)
            lms = npz['landmarks']  # (T,33,3) or (T,99)
            # aggregate per-video using mean and std
            if lms.ndim == 3:
                T = lms.shape[0]
                flat = lms.reshape(T, -1)
            else:
                flat = lms
            feat = np.concatenate([np.nanmean(flat, axis=0), np.nanstd(flat, axis=0)])
            X.append(feat)
            y.append(rec['label'])
            step_ids.append(rec['step_id'])
    # Encode step_id as frequency-based target encoding (simple)
    unique_steps = sorted(set(step_ids))
    step_map = {s: i for i, s in enumerate(unique_steps)}
    step_feat = np.array([step_map[s] for s in step_ids], dtype=np.float32).reshape(-1, 1)
    X = np.array(X, dtype=np.float32)
    X = np.hstack([X, step_feat])
    return X, np.array(y), step_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', type=Path, default=Path('datasets/manifests/train.jsonl'))
    ap.add_argument('--out', type=Path, default=Path('trained_model/model_generated.pkl'))
    args = ap.parse_args()

    X, y, step_map = load_samples(args.manifest)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model and step map
    import pickle
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        pickle.dump((clf, None, step_map), f)
    print(f"[model] saved to {args.out}")


if __name__ == '__main__':
    main()
