from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class StepInfo(BaseModel):
    id: str
    name: str
    description: str
    referenceVideoUrl: str


@router.get("/", response_model=list[StepInfo])
async def list_steps():
    """List available dance steps (reference videos)."""
    # TODO: Replace with dynamic lookup (Google Drive / GCS) based on env config.
    return [
        {
            "id": "step-001",
            "name": "Basic Hip Roll",
            "description": "A standard hip-roll step starting from front-facing position.",
            "referenceVideoUrl": "https://example.com/ref/step-001-front.mp4",
        },
        {
            "id": "step-002",
            "name": "Arm Wave",
            "description": "A simple arm wave sequence with hand articulation.",
            "referenceVideoUrl": "https://example.com/ref/step-002-front.mp4",
        },
    ]
