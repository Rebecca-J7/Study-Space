# 📚 Study Space
> An AI-powered study style quiz app that helps you discover how you learn best — and gives you personalized study strategies to match.

---

## Description

Study Space is a conversational web application powered by the Google Gemini API. Users are guided through a VARK-based learning style quiz (Visual, Auditory, Reading/Writing, Kinesthetic) via an AI chatbot. Based on their responses, the app generates a personalized learning profile and recommends tailored study strategies and tools to help them study smarter.

Built as part of a university lab series practicing agent-driven TDD (Test-Driven Development) with a professional 3-tier architecture: interface → engine → storage.

---

## Project Structure

```
study-space/                        # Root repository
├── study-space/                    # Backend (FastAPI)
│   ├── src/                        # Source code directory
│   │   ├── interface/              # User-facing chat and quiz logic
│   │   ├── engine/                 # VARK scoring and Gemini recommendation engine
│   │   └── storage/                # Session persistence and duplicate handling
│   ├── api/
│   │   └── main.py                 # FastAPI app entrypoint
│   ├── tests/                      # Test directory
│   │   ├── interface/
│   │   ├── engine/
│   │   └── storage/
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
- A Google AI Studio account with a Gemini API key ([aistudio.google.com](https://aistudio.google.com))
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

#### 3. Set Up Backend Environment Variables

Create a `.env` file inside the `study-space/` folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEET_NAME=StudySpaceResults
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

#### 4. (Optional) Google Sheets Storage

If using Google Sheets as a storage backend, place your `service_account.json` credentials file in the `study-space/` folder. This file is also excluded from version control via `.gitignore`.

#### 5. Run the Backend Locally

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at `http://localhost:8001`.

---

### Frontend Setup

#### 6. Install Node Dependencies

From the repo root:

```bash
npm install
```

#### 7. Set Up Frontend Environment Variables

Create a `.env.local` file in the repo root:

```
STUDYSPACE_BACKEND=http://localhost:8001
```

For production, set `STUDYSPACE_BACKEND` to your deployed backend URL (e.g. Railway).

#### 8. Run the Frontend Locally

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
6 passed in 0.XX s
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
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `GOOGLE_SHEET_NAME` | `StudySpaceResults` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | FastAPI, Uvicorn |
| AI Engine | Google Gemini API (`google-genai`) |
| Storage | In-memory (`SESSION_STORE`) → Google Sheets (`gspread`) |
| Testing | `pytest` |
| Auth | `google-auth`, `python-dotenv` |
| Language | Python 3.10+, TypeScript |
| Deployment | Vercel (frontend), Railway (backend) |

---

## Author

**[Rebecca Jennings]**
[UCR] — [CS180 Section 001]
[GitHub Profile](https://github.com/Rebecca-J7)
