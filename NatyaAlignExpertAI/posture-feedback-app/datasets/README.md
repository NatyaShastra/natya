# Dataset Pipeline for Natya Align Expert AI

This folder contains a simple, reproducible pipeline to build a training dataset for up to 120 dance steps.

## Folder layout
```
posture-feedback-app/
  datasets/
    raw_videos/                 # place your source videos here
      <step_id>/<angle>/<label>/<file>.mp4
      # step_id: e.g., adavu_001
      # angle: front | left | right | back (free)
      # label: correct | incorrect-<rule>
    processed/
      poses/                    # extracted MediaPipe pose landmarks (*.npz)
      videos/                   # rendered skeleton videos from landmarks
    processed/poses_aug/        # auto-generated incorrect poses (from rules)
    manifests/
      train.jsonl               # manifest for training
```

## 1) Extract poses from videos
```
python scripts/extract_poses.py --root datasets/raw_videos --out datasets/processed/poses
```

## 2) Generate incorrect poses automatically
```
python scripts/generate_incorrect_poses.py --in datasets/processed/poses --out datasets/processed/poses_aug
```
Rules: slouch, knees_in, arms_low, feet_misaligned (extend in script).

## 3) (Optional) Render skeleton multi-views
```
python scripts/render_skeleton_views.py --in datasets/processed/poses --out datasets/processed/videos --views front left right back
```

## 4) Build manifest for training
```
python scripts/build_manifest.py --in datasets/processed/poses datasets/processed/poses_aug --out datasets/manifests/train.jsonl
```

## 5) Train a classifier
```
python scripts/train_classifier.py --manifest datasets/manifests/train.jsonl --out trained_model/model_generated.pkl
```

## One command to run the whole pipeline
```
python scripts/make_dataset.py --train
```
Flags you can use:
- --skip-extract, --skip-augment, --skip-render, --skip-manifest
- Omit --train if you only want to build the dataset/manifest

## Your next steps
1) Record or collect videos and place them under `datasets/raw_videos/<step_id>/<angle>/<label>/file.mp4`.
2) Run the one-liner above to build the dataset, generate incorrect examples, render views, create the manifest, and train.
3) Inspect `datasets/processed/videos` and a few `.npz` files to validate quality.
4) Iterate on `generate_incorrect_poses.py` by adding rules that reflect real student mistakes you see most often.
5) Rerun `python scripts/make_dataset.py --train` after updates.

## Tips
- Record at least 5 clean "correct" videos per step across angles.
- Extend `generate_incorrect_poses.py` with more rule-based errors you commonly see.
- You can also place real incorrect videos in `raw_videos/.../incorrect-<rule>/` and extract as-is.
- For more realistic multi-view, consider 3D pose and Blender/Unity rendering.