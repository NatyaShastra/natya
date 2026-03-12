# Natya Posture Correction

A new posture correction solution that compares a student’s uploaded dance video against a reference set of curated step videos and returns coaching feedback.

This repository contains two main components:

- **Backend** – a FastAPI service that runs pose estimation (MediaPipe), detects the dance step, and generates coaching feedback.
- **Frontend** – a React/Vite UI that lets users pick a reference step, upload their performance, and see feedback.

## 📁 Layout

- `NatyaPostureCorrection/backend` – backend service (FastAPI + MediaPipe)
- `NatyaPostureCorrection/frontend` – frontend web app (React + Vite)

## ▶ Getting started (local dev)

### Backend

```bash
cd NatyaPostureCorrection/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd NatyaPostureCorrection/frontend
npm install
npm run dev
```

Then open http://localhost:5173.

## 🧠 Next steps

1. Replace placeholder step detection logic with a model trained on the reference videos.
2. Implement pose comparison + feedback generation.
3. Add an annotations generator (overlay on video + analytics).
4. Deploy backend (Cloud Run / ECS / App Service) and frontend (Netlify).
