import os
import tempfile
import uuid
from typing import Optional

from fastapi import UploadFile

from app.services.storage import save_analysis_result
from app.services.pose import extract_pose_sequence
from app.services.step_detection import detect_step_from_pose_sequence
from app.services.feedback import generate_feedback


class AnalysisResult:
    def __init__(
        self,
        request_id: str,
        step_id: str | None,
        summary: str,
        issues: list[dict],
        annotations_url: str | None,
    ):
        self.request_id = request_id
        self.step_id = step_id
        self.summary = summary
        self.issues = issues
        self.annotations_url = annotations_url


async def analyze_student_video(request_id: str, student_video: UploadFile, step_id: Optional[str]):
    # Save the uploaded video to a temporary file
    tmp_dir = os.environ.get("UPLOAD_DIR", "/tmp/natya_uploads")
    os.makedirs(tmp_dir, exist_ok=True)

    temp_path = os.path.join(tmp_dir, f"{request_id}_{student_video.filename}")
    with open(temp_path, "wb") as f:
        f.write(await student_video.read())

    # Extract pose sequence from student video
    try:
        pose_sequence = extract_pose_sequence(temp_path)
    except Exception as e:
        summary = (
            "Failed to extract pose landmarks from the uploaded video. "
            "Please ensure the video is clear and contains a visible full-body view."
        )
        issues = [
            {"type": "error", "message": str(e), "severity": "error"},
        ]

        result = AnalysisResult(
            request_id=request_id,
            step_id=None,
            summary=summary,
            issues=issues,
            annotations_url=None,
        )
        save_analysis_result(request_id, result)
        return result

    # Detect step if not explicitly provided
    detected_step = step_id
    if detected_step is None:
        detected_step = detect_step_from_pose_sequence(pose_sequence)

    # Generate feedback
    summary, issues = generate_feedback(pose_sequence, detected_step)

    # TODO: generate annotation video, upload somewhere, and return URL
    annotations_url = None

    result = AnalysisResult(
        request_id=request_id,
        step_id=detected_step,
        summary=summary,
        issues=issues,
        annotations_url=annotations_url,
    )

    save_analysis_result(request_id, result)

    return result
