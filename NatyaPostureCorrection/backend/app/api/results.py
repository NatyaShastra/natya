from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.storage import load_analysis_result

router = APIRouter()


class ResultPayload(BaseModel):
    requestId: str
    stepId: str | None
    summary: str
    issues: list[dict]
    annotationsUrl: str | None


@router.get("/{request_id}", response_model=ResultPayload)
async def get_result(request_id: str):
    data = load_analysis_result(request_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return data
