from fastapi import APIRouter

from app.api import steps, analyze, results

router = APIRouter()

router.include_router(steps.router, prefix="/steps", tags=["steps"])
router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
router.include_router(results.router, prefix="/results", tags=["results"])
