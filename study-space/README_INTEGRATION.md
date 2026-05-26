Study Space — Frontend ↔ Backend integration

Overview

This document explains how to run the local FastAPI backend (study-space) and connect it to the Next.js frontend in this repo. The frontend already calls the backend directly at `http://localhost:8001` from `ChatPopup`, and a Next.js proxy route is available at `/api/study-space`.

Prerequisites

- Python 3.10+ and `pip`
- Node.js 18+ and `npm`/`pnpm`/`yarn`
- Google credentials if you want recommendations and Google Sheets saving:
  - `GEMINI_API_KEY` (or Vertex AI credentials depending on your setup)
  - `GOOGLE_CLOUD_PROJECT`
  - `service_account.json` file with access to the Google Sheet named `StudySpaceResults`

Environment

Create a `.env` file in the `study-space/` folder with the following keys (example):

GEMINI_API_KEY=... 
GOOGLE_CLOUD_PROJECT=your-gcp-project
SERVICE_ACCOUNT_FILE=service_account.json

Running the backend API

From the repo root:

```bash
# install Python deps
pip install -r study-space/requirements.txt

# run the FastAPI server (from PowerShell)
$env:PYTHONPATH = 'study-space'; uvicorn study-space.api.main:app --reload --port 8001

# or (bash)
PYTHONPATH=study-space uvicorn study-space.api.main:app --reload --port 8001
```

Running the frontend

From the repo root:

```bash
npm install
npm run dev
```

Using the Next.js API proxy (optional)

You can use the Next.js proxy route to avoid CORS during development. Send POST requests to `/api/study-space/v1/process_quiz` and the route will forward them to the Python server running on `http://localhost:8001`. Set `STUDYSPACE_BACKEND` env var if the Python backend runs elsewhere.

Testing

- Open the web UI and open the chat popup. Send a message — the frontend will POST to the backend and show the raw response.
- If you want to call via the proxy, update the frontend fetch URL to `/api/study-space/v1/process_quiz` instead of `http://localhost:8001/v1/process_quiz`.

Troubleshooting

- If the backend errors about Google credentials, confirm `SERVICE_ACCOUNT_FILE` path is correct and the `StudySpaceResults` sheet exists.
- If CORS issues persist using direct fetch, use the Next.js proxy route.

What's next

- Improve UI parsing of the recommendation JSON into friendly cards.
- Securely store API keys for deployment.
