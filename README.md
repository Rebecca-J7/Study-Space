# 📚 Study Space

> An AI-powered study style quiz app that helps you discover how you learn best — and gives you personalized study strategies to match.

---

## Description

Study Space is a conversational web application powered by the Google Gemini API. Users are guided through a VARK-based learning style quiz (Visual, Auditory, Reading/Writing, Kinesthetic) via an AI chatbot. The app uses a multi-turn conversation loop with a confidence scoring system — if a response is too vague, Gemini prompts the user for more detail before scoring.

Based on quiz responses, the app generates a personalized learning profile with a visual score breakdown, dominant style identification, hardcoded core strategies, recommended tools, and Gemini-generated personalized tips tailored to the user's exact score profile.

Built as part of a university lab series practicing agent-driven TDD (Test-Driven Development) with a professional 3-tier architecture: interface → engine → storage.

---

## Features

- **Multi-turn conversation** — Gemini asks follow-up questions if your answer is too vague
- **Confidence scoring** — responses below 40% confidence trigger a follow-up loop
- **VARK score breakdown** — visual progress bars for all four learning dimensions
- **Dominant style identification** — your strongest learning modality highlighted
- **Hardcoded core strategies** — reliable, curated tips per VARK style
- **Gemini personalized tips** — dynamic advice generated from your exact score profile
- **Google Sheets storage** — quiz results saved with session ID and timestamp
- **Duplicate detection** — prevents the same session from being saved twice

---

## Project Structure

```
study-space/                        # Root repository
├── study-space/                    # Backend (FastAPI)
│   ├── src/                        # Source code directory
│   │   ├── interface/              # CLI and presentation layer
│   │   │   └── cli.py              # Multi-turn quiz session, format_response
│   │   ├── engine/                 # VARK scoring and Gemini engine
│   │   │   ├── engine.py           # Tool Use + Reflection + confidence scoring
│   │   │   └── recommender.py      # Hardcoded + Gemini personalized recommendations
│   │   └── storage/                # Session persistence
│   │       └── storage_handler.py  # Google Sheets integration + duplicate detection
│   ├── api/
│   │   └── main.py                 # FastAPI app entrypoint
│   ├── tests/                      # Test directory
│   │   ├── interface/              # 12 interface tests
│   │   ├── engine/                 # 9 engine tests
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
    │   │   └── api/study-space/    # Proxy route to backend
    │   └── components/             # React components including ChatPopup
    ├── next.config.mjs
    ├── eslint.config.mjs
    ├── package.json
    └── .env.local                  # Frontend env vars — never commit this file
```

### Key Paths

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

#### 5. (Optional) Google Sheets Storage

Place your `service_account.json` credentials file in the `study-space/` folder. This file is excluded from version control via `.gitignore`.

Share the Google Sheet named `StudySpaceResults` with the service account email as an Editor.

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
27 passed in X.XX s
```

**Test coverage by layer:**

| Layer | Tests |
|---|---|
| Storage | 3 tests |
| Recommender engine | 3 tests |
| Engine (Tool Use + Reflection + Confidence) | 9 tests |
| Interface (CLI + format_response) | 12 tests |
| **Total** | **27 tests** |

---

## How It Works

```
User types answer
    → Multi-turn loop (asks for more detail if vague)
        → Confidence check (threshold: 40%)
            → VARK scoring via Gemini
                → Reflection validates all four scores present
                    → Google Sheets storage
    ← VARK score breakdown with progress bars
    ← Dominant style identified
    ← Hardcoded core strategies + recommended tools
    ← Gemini personalized tips based on exact score profile
```

---

## Deployment

Study Space is deployed as two separate services:

| Service | Platform | Notes |
|---|---|---|
| Frontend (Next.js) | [Vercel](https://vercel.com) | Auto-deploys on push to `main` |
| Backend (FastAPI) | [Railway](https://railway.app) | Root directory set to `study-space/` |

### Vercel Environment Variables

Set the following in your Vercel project dashboard under **Settings → Environment Variables**:

| Key | Value |
|---|---|
| `STUDYSPACE_BACKEND` | Your Railway public URL (e.g. `https://study-space-production-xxxx.up.railway.app`) |

### Railway Environment Variables

Set the following in your Railway service dashboard under **Variables**:

| Key | Value |
|---|---|
| `GOOGLE_CLOUD_PROJECT` | Your GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` |
| `GOOGLE_SHEET_NAME` | `StudySpaceResults` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | FastAPI, Uvicorn |
| AI Engine | Google Gemini (`gemini-2.5-flash` via Vertex AI / Agent Platform) |
| Auth | Application Default Credentials (ADC), `google-auth` |
| Storage | In-memory (`SESSION_STORE`) → Google Sheets (`gspread`) |
| Testing | `pytest` with mocking via `unittest.mock` |
| Language | Python 3.10+, TypeScript |
| Deployment | Vercel (frontend), Railway (backend) |

---

## Author

**[Rebecca Jennings]**
[UCR] — [CS180 Section 001]
[GitHub Profile](https://github.com/Rebecca-J7)
