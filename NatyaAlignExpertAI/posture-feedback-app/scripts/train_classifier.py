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
    
    # Get number of classes and samples
    unique_classes = np.unique(y)
    n_classes = len(unique_classes)
    n_samples = len(y)
    
    print(f"[train] Found {n_samples} samples with {n_classes} unique classes")
    
    # Calculate test_size to ensure at least one sample per class
    min_test_size = max(n_classes, int(n_samples * 0.2))
    test_size = min(min_test_size, int(n_samples * 0.4))  # Cap at 40% of data
    
    # Check if we have enough samples to perform a proper split
    if n_samples <= n_classes:
        # Very small dataset - train on all data
        print("[train] WARNING: Extremely limited data. Training on all data without test evaluation.")
        X_train, y_train = X, y
        clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
        clf.fit(X_train, y_train)
        print("[train] Model trained on all data.")
    else:
        try:
            # Try manual stratification to ensure at least one sample per class
            from collections import defaultdict
            class_indices = defaultdict(list)
            for i, label in enumerate(y):
                class_indices[label].append(i)
            
            # Select indices for test set with at least one sample per class
            test_indices = []
            for cls, indices in class_indices.items():
                # Take at least one sample per class, more if possible
                samples_per_class = max(1, int(len(indices) * 0.2))
                test_indices.extend(indices[:samples_per_class])
            
            # Create train indices as the remaining indices
            all_indices = set(range(len(y)))
            train_indices = list(all_indices - set(test_indices))
            
            # Split data using these indices
            X_train, y_train = X[train_indices], y[train_indices]
            X_test, y_test = X[test_indices], y[test_indices]
            
            print(f"[train] Using custom split: {len(X_train)} train samples, {len(X_test)} test samples")
            
            # Train the model
            clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
            clf.fit(X_train, y_train)
            
            # Evaluate on test set
            y_pred = clf.predict(X_test)
            print(classification_report(y_test, y_pred))
        except Exception as e:
            print(f"[train] WARNING: {e}")
            print("[train] Falling back to training on all data")
            # Just train on all data as fallback
            X_train, y_train = X, y
            clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
            clf.fit(X_train, y_train)
            print("[train] Model trained on all data.")

    # Save model and step map
    import pickle
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        pickle.dump((clf, None, step_map), f)
    print(f"[model] saved to {args.out}")


if __name__ == '__main__':
    main()