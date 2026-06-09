# Study Space — Contract.md

This document defines the interface contracts between the three layers of Study Space:
`interface → engine → storage`

---

## Architecture Summary

| Layer | Responsibility |
|---|---|
| **Interface** | Collects user input, displays results, formats output — no AI calls, no storage access |
| **Engine** | Gemini-powered VARK scoring, confidence checking, reflection validation, recommendations, Q&A |
| **Storage** | Persists quiz results to Google Sheets, handles duplicate detection |

---

## Functionality 1: Structured VARK Quiz

### Layer Responsibilities

- **Interface:** Display 5 structured questions one at a time, collect answers, show progress indicator, prompt for elaboration if confidence is low
- **Engine:** Combine all answers, call Gemini to extract VARK scores and confidence rating, run reflection to validate all four keys are present, apply confidence threshold (40%)
- **Storage:** Save completed quiz results to Google Sheets with session ID and timestamp

### `interface → engine`

#### `extract_vark_scores(user_input: str) -> dict`
- Success (confident): `{"status": "success", "confidence": 85, "data": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20}}`
- Low confidence: `{"status": "low_confidence", "confidence": 15, "message": "Input too vague to determine learning style reliably."}`
- Failure: `{"status": "error", "message": "Could not extract scores."}`

#### `reflect_on_scores(extracted: dict) -> dict`
- Complete: `{"complete": true, "missing": []}`
- Incomplete: `{"complete": false, "missing": ["auditory", "kinesthetic"]}`

#### `process_quiz_input(session_id: str, user_input: str) -> dict`
- Success: `{"status": "success", "id": "<session_id>", "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20}, "dominant": "Visual"}`
- Exists (duplicate): `{"status": "exists", "message": "Session already recorded."}`
- Low confidence: `{"status": "low_confidence", "confidence": 15, "message": "Input too vague to determine learning style reliably."}`
- Incomplete: `{"status": "incomplete", "missing": ["reading", "kinesthetic"]}`
- Error: `{"status": "error", "message": "Could not extract scores."}`

### `engine → storage`

#### `save_quiz_progress(session_id: str, scores: dict) -> dict`
- Required score keys: `"visual"`, `"auditory"`, `"reading"`, `"kinesthetic"`
- Success: `{"status": "success", "id": "<session_id>", "saved": true}`
- Duplicate: `{"status": "exists", "message": "Session already recorded."}`
- Missing fields: `{"status": "error", "message": "Missing required score fields."}`
- Storage error: `{"status": "error", "message": "<error details>"}`

---

## Functionality 2: Personalized Study Recommendations

### Layer Responsibilities

- **Interface:** Display final VARK score breakdown with progress bars, dominant style badge, core strategies, tool list, and Gemini personalized tips
- **Engine:** Takes VARK scores and dominant style, returns hardcoded strategies + Gemini-generated personalized tips based on exact score profile
- **Storage:** Not required — recommendations are generated on demand

### `interface → engine`

#### `get_recommendations(vark_result: dict) -> dict`
- Required input keys: `"dominant"`, `"visual"`, `"auditory"`, `"reading"`, `"kinesthetic"`
- Success: 
```json
{
  "status": "success",
  "data": {
    "dominant": "Visual",
    "strategies": ["Use mind maps", "Color-code notes", "Watch video summaries"],
    "tools": ["Canva", "YouTube", "Notion", "MindMeister", "Anki"],
    "personalized_tips": ["Tip 1 from Gemini", "Tip 2", "Tip 3"]
  }
}
```
- Tied styles:
```json
{
  "status": "tied",
  "data": {
    "tied_styles": ["Visual", "Kinesthetic"],
    "strategies": ["..."],
    "tools": ["..."],
    "personalized_tips": ["..."]
  }
}
```
- Failure: `{"status": "error", "message": "Could not generate recommendations."}`

---

## Functionality 3: Post-Results Q&A

### Layer Responsibilities

- **Interface:** After results are shown, open a free chat mode where users can ask follow-up questions about their learning style or study tips; exits on `"done"` or `"quit"`
- **Engine:** Takes the user's question, dominant style, and scores; calls Gemini to generate a personalized 2–3 sentence response
- **Storage:** Not required

### `interface → engine`

#### `answer_followup(question: str, dominant: str, scores: dict) -> str`
- Success: Returns a non-empty string with personalized advice
- Empty question: Returns fallback string `"Please ask a question about your learning style or study tips!"`
- Error: Returns `"I couldn't generate an answer right now. Please try again."`

---

## Functionality 4: Quiz Retake & Profile Reset

### Layer Responsibilities

- **Interface:** "Start New Session" button clears all state and resets to the welcome screen; new session ID generated on next quiz start
- **Engine:** Reinitializes quiz state, clears accumulated context
- **Storage:** New session ID prevents duplicate detection issues; old session remains in Sheets for historical record

### `interface → engine`

#### `quiz_start() -> dict`
- Success: `{"session_id": "<uuid>", "question": "Q1: ...", "question_number": 1, "total_questions": 5}`

---

## API Endpoints (FastAPI Backend)

| Endpoint | Method | Description |
|---|---|---|
| `/v1/quiz/start` | POST | Start a new quiz session, returns Q1 and session_id |
| `/v1/quiz/answer` | POST | Submit answer to current question, returns next question or final result |
| `/v1/quiz/elaborate` | POST | Submit elaboration when confidence is low, re-scores combined input |
| `/v1/quiz/followup` | POST | Ask a follow-up question after results, returns Gemini answer |
| `/v1/recommendations` | POST | Get VARK-based hardcoded + Gemini recommendations |
| `/v1/process_quiz` | POST | Legacy single-turn quiz endpoint |
| `/v1/debug` | GET | Health check for Gemini connection |

### `/v1/quiz/start`
```json
// Response
{
  "session_id": "uuid",
  "question": "Q1: When learning something new...",
  "question_number": 1,
  "total_questions": 5
}
```

### `/v1/quiz/answer`
```json
// Request
{ "session_id": "uuid", "answer": "I prefer watching videos and diagrams." }

// Response — in progress
{ "session_id": "uuid", "question": "Q2: ...", "question_number": 2, "total_questions": 5, "status": "in_progress" }

// Response — complete
{ "session_id": "uuid", "status": "success", "result": { "status": "success", "scores": {...}, "dominant": "Visual" } }
```

### `/v1/quiz/elaborate`
```json
// Request
{ "session_id": "uuid", "answer": "I love watching YouTube tutorials and drawing mind maps." }

// Response
{ "session_id": "uuid", "status": "success", "result": { "status": "success", "scores": {...}, "dominant": "Visual" } }
```

### `/v1/quiz/followup`
```json
// Request
{ "session_id": "uuid", "question": "How should I study for math exams?" }

// Response
{ "session_id": "uuid", "answer": "As a visual learner, try drawing diagrams..." }
```

---

## Status Code Reference

| Status | Layer | Meaning |
|---|---|---|
| `"success"` | All | Operation completed successfully |
| `"exists"` | Storage | Duplicate session ID detected |
| `"error"` | All | Unexpected failure |
| `"low_confidence"` | Engine | Gemini confidence below 40% threshold |
| `"incomplete"` | Engine | One or more VARK keys missing from extraction |
| `"in_progress"` | API | Quiz still has remaining questions |
| `"tied"` | Engine | Two or more VARK styles share the highest score |
