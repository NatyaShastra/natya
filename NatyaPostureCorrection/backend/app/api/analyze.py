from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from uuid import uuid4

from app.services.analysis import analyze_student_video

router = APIRouter()


class AnalyzeResponse(BaseModel):
    requestId: str
    stepId: str | None
    message: str


@router.post("/", response_model=AnalyzeResponse)
async def analyze(
    student_video: UploadFile = File(...),
    step_id: str | None = Form(None),
):
    """Analyze the uploaded student video and return an analysis request id."""

    if student_video.content_type not in {"video/mp4", "video/webm", "video/quicktime"}:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    request_id = str(uuid4())

    # NOTE: In the MVP this will be synchronous, but we store the result for later retrieval
    # and allow the UI to poll /results/{request_id}.
    result = await analyze_student_video(request_id, student_video, step_id)

    return AnalyzeResponse(
        requestId=request_id,
        stepId=result.step_id,
        message="Analysis complete (use /api/results/{requestId} to fetch details).",
    )
