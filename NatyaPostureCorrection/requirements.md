# Natya Posture Correction — Requirements

## 🎯 Project Vision
Build a web-based posture correction system for dance learners that:
- Lets the student *view a curated reference dance step* (one “perfect” video per step)
- Lets the student *upload their own 10s performance* of that step
- Automatically *identifies which step the student performed*
- Compares the student’s posture against the reference step (normalized for height/age/shape)
- Produces **clear, actionable feedback** (visual + text) that a student or parent can easily understand
- Provides an annotated output (video +/or frame snapshots) highlighting the key posture mistakes
- Works as a deployable web service (frontend + backend APIs) that can be hosted (Netlify + cloud backend)

---

## 📌 MVP Scope (what this project will deliver first)
1. **Reference step library**
   - Reference (base) videos are stored in Google Drive / Google Cloud Storage and are **managed by the project owner** (not uploaded by users)
   - Each step has one main “reference video” shown in the UI (front view) and multiple angle videos (side, top, etc.) stored for model training/analysis.

2. **Student upload flow**
   - Student selects a step in the UI
   - Uploads a 5–10 second video of their performance
   - The backend runs posture analysis & returns feedback

3. **Step automatic recognition**
   - Backend identifies which step the student is performing (based on trained step classifier)
   - If the user selected a step, use that as a hint; otherwise automatically detect

4. **Posture comparison + feedback**
   - Use pose-estimation (MediaPipe / BlazePose) to extract skeleton keypoints
   - Normalize by body size/height/angle
   - Compare student keypoints → reference keypoints
   - Generate a feedback report (text + optional annotated imagery)

5. **Web UI**
   - Shows reference video + upload form
   - Displays feedback results clearly (e.g., “Your shoulder is tilted left by 10°”, “Raise your right knee”)

---

## ✅ Functional Requirements
### 1) Reference library (controlled by owner)
- A curated set of reference videos exists in Google Drive / GCS
- Each dance step includes:
  - 1 “primary” reference video (front view, shown in UI)
  - Multiple auxiliary videos (side, top, etc.) for training/analysis
- The backend should be able to fetch these reference files (public URLs / signed URLs) at runtime

### 2) Step selection + automatic recognition
- The backend should support:
  - Explicit step selection (user selects step before uploading)
  - Implicit step recognition (system classifies the user’s upload against available steps)

### 3) Pose analysis + comparison
- Extract per-frame skeleton keypoints from both:
  - Reference video (precomputed during model training/batch processing)
  - Student video (runtime)
- Normalize for user body size:
  - Use a body reference length (e.g., shoulder width, hip-to-shoulder) to scale the pose
  - Align based on torso/pelvis to remove rotation/translation differences
- Compare using a mix of:
  - Joint angle differences (e.g., elbows, knees, spine tilt)
  - Keypoint distance differences after normalization
  - Time alignment (DTW or simplified frame-matching)

### 4) Feedback generation
- Produce final output entries like:
  - “Your left knee is bent 18° more than the reference”
  - “Your upper back is tilted forward; keep your spine straight”
  - “Your right arm is lower than reference; raise by ~15°”
- May include a short “fix recommendation” per mistake
- Provide a “summary score” or “pass/fail guidance” (optional)

### 5) Presentation (UI)
- Display reference video and optionally reference keypoint overlay
- Show student video with keypoint overlay and highlight error areas
- Provide “jump to frame” links where the biggest errors occur

---

## 🧩 High-level architecture (recommended)
### 1) Frontend (Web UI)
- React + Vite
- Hosted on **Netlify** (static site)
- Uploads student video + selected step to backend endpoint
- Displays result (JSON + video URLs)

### 2) Backend API (Processing server)
- FastAPI (recommended) or Flask
- Endpoints:
  - `GET /steps` → list of available steps + reference video URLs
  - `POST /analyze` → upload student video + (optional) chosen step
  - `GET /results/{id}` → fetch analysis results
- Processing flow:
  1. Store uploaded video temporarily
  2. Run pose extraction on uploaded video (MediaPipe)
  3. Match against reference step (run classifier or best-match comparison)
  4. Compute deviation metrics + generate feedback
  5. Return JSON response with feedback + annotation URLs

### 3) Reference model / training
- Reference videos (Google Drive) are used to train:
  - A **step classifier** (to identify which step the user is performing)
  - A **pose reference database** (precomputed keypoints per step)
- Training can be batch/offline (run manually or via a scheduled job)
- The trained model(s) are then stored in the backend (e.g., `models/`)

### 4) Deployment
- Frontend: Netlify (static, can be linked to GitHub)
- Backend: containerized service (Cloud Run / ECS / App Service)
- Storage:
  - Temporary uploads → local disk or cloud bucket
  - Reference videos → Google Drive / GCS (public URLs)
  - Optional: store results/annotations in a DB (SQLite / PostgreSQL)

---

## 🧰 Spec Kit setup (starter guide)
> This section assumes you want to use a “spec kit” workflow to plan and track tasks.

> **Note:** In this repository we have already scaffolded the backend+frontend and created a `requirements.md` spec file. The remainder of the work can be tracked using either GitHub Issues/Projects or a lightweight spec file system (see below).

### 1) Project planning (recommended)
Use GitHub Issues (or Projects) to track tasks, or create a simple `spec/` directory with YAML/Markdown task definitions.

Example markdown task list (in `spec/tasks.md`):
```md
- [ ] Backend: load pose landmarker model from `.task` file
- [ ] Backend: implement step recognition using reference pose data
- [ ] Backend: compute pose comparison metrics (angles, normalized joints)
- [ ] Backend: generate narrative feedback using OpenAI
- [ ] Frontend: implement upload & results workflow
- [ ] Frontend: display annotated video + issue highlights
```

### 2) Configuration & env values (important)
Your environment will need values like:
- `POSE_LANDMARKER_MODEL_PATH` (required) — path to a MediaPipe `.task` model file used for pose extraction
- `REFERENCE_VIDEO_BASE_URL` — public URL base for your reference videos (Google Drive / GCS)
- `OPENAI_API_KEY` — (optional) for narrative coaching output via OpenAI
- `UPLOAD_DIR` / `RESULTS_DIR` — locations for temporary storage and results

Put these in a `.env` file or your hosting provider’s environment config.

### 3) Next implementation steps (recommended priorities)
1. **Acquire or generate the MediaPipe pose landmarker `.task` model** and store it in `backend/models/`.
2. **Implement reference pose ingestion** (precompute pose sequences for each reference step).
3. **Implement step detection** (match uploaded video to closest reference step).
4. **Implement comparison & feedback** (angle deviations, joint alignment, narrative output).
5. **Add annotated video output** (skeleton overlays, keyframe highlights).
6. **Deploy backend + frontend** (Cloud Run/ECS + Netlify) with environment configuration.

---

## ✅ What was created (in this workspace)
- **New project folder:** `NatyaPostureCorrection/`
- **Requirements doc:** `NatyaPostureCorrection/requirements.md` (this file)

---

## Next steps (what you should do now)
1. Confirm the *architecture decisions* (backend stack, pose library, training strategy)
2. Confirm your *spec kit tooling* (exact CLI name + command set)
3. Then we can create the **initial project scaffold** (frontend + backend glue) and start implementing the first tasks.
