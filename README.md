# 📚 Study Space

> An AI-powered study style quiz app that helps you discover how you learn best — and gives you personalized study strategies to match.

---

## Description

Study Space is a conversational web application powered by the Google Gemini API. Users are guided through a structured 5-question VARK-based learning style quiz (Visual, Auditory, Reading/Writing, Kinesthetic) via an AI chatbot. The app uses a multi-turn conversation loop with a confidence scoring system — if responses are too vague, Gemini prompts the user for more detail before scoring.

Based on quiz responses, the app generates a personalized learning profile with a visual score breakdown, dominant style identification, hardcoded core strategies, recommended tools, and Gemini-generated personalized tips tailored to the user's exact score profile. After results are shown, users can continue in a free Q&A session to ask follow-up questions about their learning style.

Built as part of a university lab series (CS180) practicing agent-driven TDD (Test-Driven Development) with a professional 3-tier architecture: interface → engine → storage.

---

## Features

- **Structured 5-question quiz** — guided questions covering all four VARK dimensions
- **Multi-turn confidence loop** — vague responses trigger elaboration prompts before scoring
- **Confidence scoring** — responses below 40% confidence are flagged for more detail
- **VARK score breakdown** — visual progress bars for all four learning dimensions
- **Dominant style identification** — your strongest learning modality highlighted
- **Hardcoded core strategies** — reliable, curated tips per VARK style
- **Gemini personalized tips** — dynamic advice generated from your exact score profile
- **Post-results Q&A** — free chat session after results to ask follow-up study questions
- **Google Sheets storage** — quiz results saved with session ID and timestamp
- **Duplicate detection** — prevents the same session from being saved twice

---

## Key Paths

| Resource | Path |
|---|---|
| Backend source code | `study-space/src/` |
| Frontend source code | `src/` |
| Tests | `study-space/tests/` |
| Requirement specification | `study-space/FUNCTIONALITY.md` |
| Design document | `study-space/CONTRACT.md` |

---

## Demo Video

> 🎥 [Link to demo video — add when available]

---

## Project Structure

```
study-space/                        # Root repository
├── study-space/                    # Backend (FastAPI)
│   ├── src/                        # Source code directory
│   │   ├── interface/              # Presentation layer
│   │   │   └── cli.py              # Structured quiz, multi-turn loop, format_response, Q&A
│   │   ├── engine/                 # Logic layer
│   │   │   ├── engine.py           # Tool Use + Reflection + confidence scoring + followup Q&A
│   │   │   └── recommender.py      # Hardcoded + Gemini personalized recommendations
│   │   └── storage/                # Storage layer
│   │       └── storage_handler.py  # Google Sheets integration + duplicate detection
│   ├── api/
│   │   └── main.py                 # FastAPI app entrypoint with quiz endpoints
│   ├── tests/                      # Test directory
│   │   ├── interface/              # 23 interface tests
│   │   ├── engine/                 # 11 engine tests
│   │   └── storage/                # 3 storage tests
│   ├── FUNCTIONALITY.md            # Requirement specification (core functionalities A–D)
│   ├── CONTRACT.md                 # Design document (API contracts and data shapes)
│   ├── AGENT_PROMPTS.md            # Gemini coding agent prompts and guardrails
│   ├── requirements.txt
│   ├── conftest.py
│   ├── pytest.ini
│   ├── Procfile                    # Railway deployment entrypoint
│   ├── agent.py
│   └── .env                        # API keys — never commit this file
└── (frontend — Next.js)            # Frontend source code directory
    ├── src/
    │   ├── app/                    # Next.js App Router pages and API routes
    │   │   └── api/study-space/    # Catch-all proxy route to backend
    │   └── components/             # React components including ChatPopup
    ├── next.config.mjs
    ├── eslint.config.mjs
    ├── package.json
    └── .env.local                  # Frontend env vars — never commit this file
```

---

## Architecture Overview

Study Space follows a strict 3-tier architecture:

```
┌─────────────────────────────────────────────┐
│              Interface Layer                 │
│  src/interface/cli.py · api/main.py          │
│  ChatPopup.tsx (Next.js frontend)            │
│  Collects user input, formats output         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│               Engine Layer                   │
│  src/engine/engine.py                        │
│  Tool Use: Gemini extracts VARK scores       │
│  Reflection: validates scores before saving  │
│  Confidence: flags vague input < 40%         │
│  src/engine/recommender.py                   │
│  Generates hardcoded + Gemini tips           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│               Storage Layer                  │
│  src/storage/storage_handler.py              │
│  Google Sheets via gspread                   │
│  Duplicate session detection                 │
│  Credentials via service account or ADC      │
└─────────────────────────────────────────────┘
```

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/v1/quiz/start` | POST | Start a new quiz session, returns Q1 |
| `/v1/quiz/answer` | POST | Submit answer, returns next question or result |
| `/v1/quiz/elaborate` | POST | Submit elaboration when confidence is low |
| `/v1/quiz/followup` | POST | Ask a follow-up question after results |
| `/v1/recommendations` | POST | Get VARK-based recommendations |
| `/v1/process_quiz` | POST | Legacy single-turn quiz endpoint |
| `/v1/debug` | GET | Health check for Gemini connection |

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 20+
- A Google Cloud project with Gemini Enterprise Agent Platform access
- Application Default Credentials (ADC) configured via `gcloud`
- Anaconda or a Python virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/rebecca-j7/study-space.git
cd study-space
```

---

### Backend Setup

#### 2. Install Python Dependencies

```bash
cd study-space
pip install -r requirements.txt
```

#### 3. Configure Application Default Credentials (ADC)

```bash
bash <(curl -sSL https://storage.googleapis.com/cloud-samples-data/adc/setup_adc.sh)
```

#### 4. Set Up Backend Environment Variables

Create a `.env` file inside the `study-space/` folder:

```
GOOGLE_CLOUD_PROJECT=your_project_id_here
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_SHEET_NAME=StudySpaceResults
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

#### 5. Google Sheets Storage

Place your `service_account.json` credentials file in the `study-space/` folder. This file is excluded from version control via `.gitignore`.

Create a Google Sheet named `StudySpaceResults` and share it with the service account email as an Editor. Add these headers in row 1:

```
session_id | visual | auditory | reading | kinesthetic | timestamp
```

#### 6. Run the CLI

```bash
python -m src.interface.cli
```

#### 7. Run the Backend API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at `http://localhost:8001`.

---

### Frontend Setup

#### 8. Install Node Dependencies

From the repo root:

```bash
npm install
```

#### 9. Set Up Frontend Environment Variables

Create a `.env.local` file in the repo root:

```
STUDYSPACE_BACKEND=http://localhost:8001
```

For production, set `STUDYSPACE_BACKEND` to your deployed Railway backend URL.

#### 10. Run the Frontend

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

---

## Running the Tests

```bash
cd study-space
pytest -q
```

Expected output when all tests pass:

```
40 passed in X.XX s
```

**Test coverage by layer:**

| Layer | File | Tests |
|---|---|---|
| Storage | `tests/storage/test_storage.py` | 3 tests |
| Recommender | `tests/engine/test_recommender.py` | 3 tests |
| Engine | `tests/engine/test_engine.py` | 11 tests |
| Interface | `tests/interface/test_interface.py` | 23 tests |
| **Total** | | **40 tests** |

**What is tested:**

- Storage: happy path save, duplicate detection, missing fields
- Engine: VARK extraction, reflection validation, confidence threshold, low confidence blocking storage, post-results Q&A
- Interface: all format_response statuses, run_session flow, structured quiz flow, vague answer elaboration loop, post-results Q&A, quit/done handling

---

## How It Works

```
User clicks "Start Quiz"
    → POST /v1/quiz/start → returns Q1
        → User answers Q1–Q5
            → POST /v1/quiz/answer (×5)
                → After Q5: Gemini extracts VARK scores
                    → Confidence check (threshold: 40%)
                        → If low: POST /v1/quiz/elaborate
                        → If confident: Reflection validates scores
                            → POST to Google Sheets storage
    ← VARK score breakdown with progress bars
    ← Dominant style identified
    ← Hardcoded core strategies + recommended tools
    ← Gemini personalized tips
        → Post-results Q&A loop
            → POST /v1/quiz/followup
            ← Gemini answers with style-specific advice
        → User types 'done' → session ends
```

---

## Deployment

Study Space is deployed as two separate services:

| Service | Platform | URL |
|---|---|---|
| Frontend (Next.js) | [Vercel](https://vercel.com) | Auto-deploys on push to `main` |
| Backend (FastAPI) | [Railway](https://railway.app) | Root directory set to `study-space/` |

### Vercel Environment Variables

| Key | Value |
|---|---|
| `STUDYSPACE_BACKEND` | Your Railway public URL (e.g. `https://study-space-production-xxxx.up.railway.app`) |

### Railway Environment Variables

| Key | Value |
|---|---|
| `GOOGLE_CLOUD_PROJECT` | Your GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` |
| `GOOGLE_SHEET_NAME` | `StudySpaceResults` |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Full contents of `service_account.json` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | FastAPI, Uvicorn |
| AI Engine | Google Gemini (`gemini-2.5-flash` via Vertex AI / Agent Platform) |
| Auth | Application Default Credentials (ADC), `google-auth`, service account JSON |
| Storage | Google Sheets (`gspread`) with in-memory session state |
| Testing | `pytest` with mocking via `unittest.mock` |
| Language | Python 3.10+, TypeScript |
| Deployment | Vercel (frontend), Railway (backend) |

---

## Author

**[Rebecca Jennings]**
[UCR] — [CS180 Section 001]
[GitHub Profile](https://github.com/Rebecca-J7)
