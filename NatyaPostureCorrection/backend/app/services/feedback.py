from typing import Tuple, List, Dict


def generate_feedback(pose_sequence: list[dict], step_id: str | None) -> Tuple[str, List[Dict]]:
    """Generate coaching feedback based on the pose sequence and detected step."""

    # TODO: Replace this placeholder with real comparison logic
    # against the reference pose sequence for the detected step.
    if not pose_sequence:
        return (
            "No pose data could be detected in the uploaded video. Please try again with a clearer video.",
            [],
        )

    summary = "Your video was analyzed successfully. The step appears to be recognized as: {}".format(
        step_id or "unknown"
    )

    issues = [
        {
            "type": "posture",
            "message": "This is a placeholder feedback item. Replace with real posture analysis.",
            "severity": "info",
        }
    ]

    return summary, issues
