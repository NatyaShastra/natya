#!/usr/bin/env python3
"""
Train a strict classifier for Bharatanatyam validation using the new manifest and augmented data.
"""
import argparse
from pathlib import Path
import pickle
from train_classifier import load_samples
from sklearn.ensemble import RandomForestClassifier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', type=Path, default=Path('datasets/manifests/train_strict.jsonl'))
    ap.add_argument('--out', type=Path, default=Path('trained_model/model_strict.pkl'))
    args = ap.parse_args()

    X, y, step_map = load_samples(args.manifest)
    clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
    clf.fit(X, y)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        pickle.dump((clf, None, step_map), f)
    print(f"[model] saved to {args.out}")

if __name__ == '__main__':
    main()
