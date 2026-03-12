# Natya Posture Correction — Frontend

A React + Vite frontend for the Natya Posture Correction application.

## ✅ Running locally

1. Install dependencies:

```bash
npm install
```

2. Run the dev server:

```bash
npm run dev
```

This will run on http://localhost:5173 and proxy API requests to http://localhost:8000.

## 📦 Build for production

```bash
npm run build
```

## 📌 What it does

- Fetches the available dance steps (reference videos) from `/api/steps`
- Lets the user pick a step and upload a 10s video
- Submits the video to `/api/analyze`
- Shows results retrieved from `/api/results/{requestId}`
