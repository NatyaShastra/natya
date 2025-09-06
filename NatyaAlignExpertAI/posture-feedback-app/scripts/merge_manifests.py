import json
from pathlib import Path

def merge_manifests(manifest_paths, out_path):
    records = []
    for manifest in manifest_paths:
        with open(manifest, 'r') as f:
            for line in f:
                records.append(json.loads(line))
    # Remove duplicates based on npz path and label
    seen = set()
    merged = []
    for rec in records:
        key = (rec['npz'], rec.get('label', ''))
        if key not in seen:
            merged.append(rec)
            seen.add(key)
    with open(out_path, 'w') as f:
        for rec in merged:
            f.write(json.dumps(rec) + '\n')
    print(f"Merged manifest written to {out_path} with {len(merged)} samples.")

if __name__ == "__main__":
    manifest1 = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/manifests/train.jsonl")
    manifest2 = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/manifests/train_strict.jsonl")
    out_path = Path("/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/manifests/train_merged.jsonl")
    merge_manifests([manifest1, manifest2], out_path)
