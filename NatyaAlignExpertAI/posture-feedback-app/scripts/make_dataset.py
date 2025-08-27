#!/usr/bin/env python3
"""
One-click dataset builder for Natya Align Expert AI.
Runs: extract poses -> generate incorrect -> render views -> build manifest -> (optional) train
"""
import argparse
import subprocess
from pathlib import Path

ROOT = Path('/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app')
DATA = ROOT / 'datasets'
SCRIPTS = ROOT / 'scripts'


def run(cmd):
    print(f"\n$ {' '.join(cmd)}\n")
    subprocess.check_call(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-extract', action='store_true')
    ap.add_argument('--skip-augment', action='store_true')
    ap.add_argument('--skip-render', action='store_true')
    ap.add_argument('--skip-manifest', action='store_true')
    ap.add_argument('--train', action='store_true', help='Train after manifest build')
    args = ap.parse_args()

    # 1) Extract landmarks
    if not args.skip_extract:
        run(['python', str(SCRIPTS / 'extract_poses.py'), '--root', str(DATA / 'raw_videos'), '--out', str(DATA / 'processed/poses')])

    # 2) Generate incorrect poses
    if not args.skip_augment:
        run(['python', str(SCRIPTS / 'generate_incorrect_poses.py'), '--in', str(DATA / 'processed/poses'), '--out', str(DATA / 'processed/poses_aug')])

    # 3) Render skeleton multi-views (optional but useful for QA/visualization)
    if not args.skip_render:
        run(['python', str(SCRIPTS / 'render_skeleton_views.py'), '--in', str(DATA / 'processed/poses'), '--out', str(DATA / 'processed/videos'), '--views', 'front', 'left', 'right', 'back'])

    # 4) Build manifest
    if not args.skip_manifest:
        run(['python', str(SCRIPTS / 'build_manifest.py'), '--in', str(DATA / 'processed/poses'), str(DATA / 'processed/poses_aug'), '--out', str(DATA / 'manifests/train.jsonl')])

    # 5) Train
    if args.train:
        run(['python', str(SCRIPTS / 'train_classifier.py'), '--manifest', str(DATA / 'manifests/train.jsonl'), '--out', str(ROOT / 'trained_model/model_generated.pkl')])


if __name__ == '__main__':
    main()
