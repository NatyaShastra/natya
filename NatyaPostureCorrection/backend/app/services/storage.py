import json
import os
from typing import Optional

RESULTS_DIR = os.environ.get("RESULTS_DIR", "/tmp/natya_results")


def save_analysis_result(request_id: str, result):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, f"{request_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "requestId": result.request_id,
                "stepId": result.step_id,
                "summary": result.summary,
                "issues": result.issues,
                "annotationsUrl": result.annotations_url,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def load_analysis_result(request_id: str) -> Optional[dict]:
    path = os.path.join(RESULTS_DIR, f"{request_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
