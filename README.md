# 📚 Study Space

> An AI-powered study style quiz app that helps you discover how you learn best — and gives you personalized study strategies to match.

---

## Description

Study Space is a conversational web application powered by the Google Gemini API. Users are guided through a VARK-based learning style quiz (Visual, Auditory, Reading/Writing, Kinesthetic) via an AI chatbot. Based on their responses, the app generates a personalized learning profile and recommends tailored study strategies and tools to help them study smarter.

Built as part of a university lab series practicing agent-driven TDD (Test-Driven Development) with a professional 3-tier architecture: interface → engine → storage.

---

## Figma

Design in progress with FIGMA <br />
[Study Space Design File](https://www.figma.com/design/inir9GAH6v3iOJ7RU0tPKn/Pomodoro-Timer-Website?node-id=0-1&t=SL0U6Fc32FEbhVOj-1)

---

## Project Structure

```
study-space/
├── src/                        # Source code directory
│   ├── interface/              # User-facing chat and quiz logic
│   ├── engine/                 # VARK scoring and Gemini recommendation engine
│   └── storage/                # Session persistence and duplicate handling
├── tests/                      # Test directory
│   ├── interface/
│   ├── engine/
│   └── storage/
├── FUNCTIONALITY.md            # Requirement specification (core functionalities A–D)
├── CONTRACT.md                 # Design document (API contracts and data shapes)
├── AGENT_PROMPTS.md            # Gemini coding agent prompts and guardrails
├── requirements.txt
├── conftest.py
├── pytest.ini
├── agent.py
└── .env                        # API keys — never commit this file
```

### Key Paths

| Resource | Path |
|---|---|
| Source code | `src/` |
| Tests | `tests/` |
| Requirement specification | `FUNCTIONALITY.md` |
| Design document | `CONTRACT.md` |

---

## Demo Video

> 🎥 [Link to demo video — add when available]

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- A Google AI Studio account with a Gemini API key ([aistudio.google.com](https://aistudio.google.com))
- Anaconda or a Python virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/rebecca-j7/study-space.git
cd study-space
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEET_NAME=StudySpaceResults
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 4. (Optional) Google Sheets Storage

If using Google Sheets as a storage backend, place your `service_account.json` credentials file in the project root. This file is also excluded from version control via `.gitignore`.

---

## Running the Tests

```bash
pytest -q
```

Expected output when all tests pass:

```
6 passed in 0.XX s
```

---

## Running the App

> 🚧 Interface layer under active development — instructions will be updated here once the chat UI is complete.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Engine | Google Gemini API (`google-genai`) |
| Storage | In-memory (`SESSION_STORE`) → Google Sheets (`gspread`) |
| Testing | `pytest` |
| Auth | `google-auth`, `python-dotenv` |
| Language | Python 3.10+ |

---

## Author

**[Rebecca Jennings]**
[UCR] — [CS180 Section 001]
[GitHub Profile](https://github.com/Rebecca-J7)
