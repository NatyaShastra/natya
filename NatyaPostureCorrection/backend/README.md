# Natya Posture Correction — Backend

This backend provides an API for extracting pose data from uploaded videos, auto-detecting dance steps, and generating coaching feedback.

## 🧱 Architecture Overview
- **FastAPI** backend (`app/main.py`) exposes:
  - `GET /health` - health check
  - `GET /api/steps` - list available dance steps (reference video URLs)
  - `POST /api/analyze` - upload a student video for analysis
  - `GET /api/results/{requestId}` - fetch analysis results

- **Pose extraction** is done using **MediaPipe** (via `app/services/pose.py`)
- **Step detection** and **feedback generation** are currently stubs and should be replaced with real models.

## 🚀 Run locally

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example env file and configure required values:
   ```bash
   cp .env.example .env
   ```

   - `POSE_LANDMARKER_MODEL_PATH`: Path to the MediaPipe `.task` pose landmarker model.
     - Example: `/workspaces/natya/NatyaPostureCorrection/backend/models/pose_landmarker.task`
   - `REFERENCE_VIDEO_BASE_URL`: Base URL for your reference videos (Google Drive / GCS).
   - `OPENAI_API_KEY`: (optional) for narrative coaching output.

4. Run the API server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 🧩 Next implementation steps
- Implement real step detection using reference videos (stored in Google Drive / GCS).
- Implement comparison logic between student pose sequence and the reference pose sequence.
- Create an annotations generator (overlay skeleton + corrections) and store it in a shareable location.
- Integrate OpenAI (or similar) for narrative coaching output.
