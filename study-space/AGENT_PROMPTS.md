# Study Space — Gemini Agent Prompts
 
This file contains all agent prompts used to generate Study Space's implementation via AI coding agents, along with guardrail reminders for correcting agent output.
 
---
 
## Prompt A: Storage Handler
 
Create `src/storage/storage_handler.py` for a study style quiz app called Study Space.
 
Implement:
```
save_quiz_progress(session_id: str, scores: dict) -> dict
```
 
Rules:
- Load credentials from environment variable `GOOGLE_APPLICATION_CREDENTIALS_JSON` first (Railway/production), fall back to `service_account.json` file (local)
- Required score keys: "visual", "auditory", "reading", "kinesthetic"
- Missing key → return `{"status": "error", "message": "Missing required score fields."}`
- Duplicate session_id → return `{"status": "exists", "message": "Session already recorded."}`
- Success → return `{"status": "success", "id": "<session_id>", "saved": true}`
- Return ONLY: "success", "exists", "error" — no other status values
- Use `GOOGLE_SHEET_NAME` env var for sheet name, default to `"StudySpaceResults"`
---
 
## Prompt B: Engine — Recommendations
 
Create `src/engine/recommender.py` for Study Space.
 
Implement:
```
get_recommendations(vark_result: dict) -> dict
```
 
Rules:
- Use `vertexai` and `GenerativeModel("gemini-2.5-flash")` — do NOT use deprecated `google.generativeai`
- Load `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` from `.env`
- Required input keys: "dominant", "visual", "auditory", "reading", "kinesthetic"
- Include hardcoded strategies and tools for each VARK style as a fallback base
- Call Gemini to generate 3 personalized tips based on the exact score profile
- If two styles are tied, return both with combined strategies
- Success → `{"status": "success", "data": {"dominant": "...", "strategies": [...], "tools": [...], "personalized_tips": [...]}}`
- Tied → `{"status": "tied", "data": {"tied_styles": [...], "strategies": [...], "tools": [...], "personalized_tips": [...]}}`
- Failure → `{"status": "error", "message": "Could not generate recommendations."}`
- Return ONLY: "success", "tied", "error"
---
 
## Prompt C: Engine — Full Chain (Tool Use + Reflection + Confidence)
 
Create `src/engine/engine.py` for a study style quiz app called Study Space.
 
CRITICAL: Use ONLY `import vertexai` and `from vertexai.generative_models import GenerativeModel` — do NOT use deprecated `google.generativeai` or `google.genai` with API keys.
 
Implement these four functions:
 
```
1. _get_client() -> GenerativeModel
2. extract_vark_scores(user_input: str) -> dict
3. reflect_on_scores(extracted: dict) -> dict
4. process_quiz_input(session_id: str, user_input: str) -> dict
5. answer_followup(question: str, dominant: str, scores: dict) -> str
```
 
Rules:
- Import at the TOP of the file:
  ```python
  import vertexai
  from vertexai.generative_models import GenerativeModel
  from src.storage.storage_handler import save_quiz_progress
  ```
- Load `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` from `.env` using python-dotenv
- Initialize model lazily: `def _get_client(): vertexai.init(...); return GenerativeModel("gemini-2.5-flash")`
- REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]
- CONFIDENCE_THRESHOLD = 40
`extract_vark_scores` (Tool Use pattern):
- Call `model.generate_content(prompt)` where prompt asks for JSON with 5 keys: visual, auditory, reading, kinesthetic (sum to 100) + confidence (0–100)
- Strip markdown fences before parsing JSON
- If confidence < CONFIDENCE_THRESHOLD → return `{"status": "low_confidence", "confidence": <n>, "message": "..."}`
- Success → return `{"status": "success", "confidence": <n>, "data": {"visual": ..., "auditory": ..., "reading": ..., "kinesthetic": ...}}`
- On any failure → return `{"status": "error", "message": "Could not extract scores."}`
`reflect_on_scores` (Reflection pattern):
- No Gemini call — check locally whether all REQUIRED_KEYS are present
- Return `{"complete": True, "missing": []}` if all keys present
- Return `{"complete": False, "missing": ["key1", ...]}` if any keys missing
`process_quiz_input` (Full chain):
- Call extract_vark_scores(user_input)
- If low_confidence → return the low_confidence result immediately, do NOT call save_quiz_progress
- If error → return incomplete with all keys missing
- Call reflect_on_scores on extracted data
- If incomplete → return `{"status": "incomplete", "missing": [...]}` and do NOT call save_quiz_progress
- If complete → call save_quiz_progress(session_id, scores)
- On success/exists → return `{"status": "...", "id": "...", "scores": {...}, "dominant": "<max style>"}`
- Return ONLY: "success", "exists", "error", "incomplete", "low_confidence"
`answer_followup` (Post-Results Q&A):
- If question is empty → return fallback string without calling Gemini
- Call Gemini with a prompt framing the user as a `{dominant}` learner with their exact scores
- Return a 2–3 sentence personalized answer as a plain string
- On error → return friendly error string
---
 
## Prompt D: Interface Layer — CLI
 
Create `src/interface/cli.py` for a study style quiz app called Study Space.
 
Implement these functions:
 
```
1. format_response(result: dict) -> str
2. run_session(process_fn=process_quiz_input)
3. run_quiz(process_fn=process_quiz_input)
4. run_quiz_with_followup(process_fn=process_quiz_input, followup_fn=None)
```
 
Rules:
- Import at the TOP of the file:
  ```python
  from src.engine.engine import process_quiz_input
  ```
- All functions must accept `process_fn` as a parameter for dependency injection — never call `process_quiz_input` directly inside loops
- `format_response` must handle: "success", "exists", "incomplete", "error", "low_confidence", and unknown statuses
- No Gemini calls, no gspread access — interface layer only collects input and formats output
- Generate a unique session_id using `uuid.uuid4()` inside session functions
- If user input is empty → print warning and return
- `run_quiz` asks 5 structured questions, combines all answers, scores once
- `run_quiz_with_followup` runs the 5-question quiz, handles low confidence elaboration loop, then opens post-results Q&A
- Low confidence loop: if result is "low_confidence", prompt for elaboration; if user types "done" force score; if "quit"/"exit" end session
- Post-results Q&A: loop accepting free-text questions, call followup_fn, exit on "done"/"quit"
---
 
## Prompt E: FastAPI Backend
 
Create `api/main.py` for Study Space.
 
Implement these endpoints:
 
```
POST /v1/quiz/start       → start session, return Q1
POST /v1/quiz/answer      → submit answer, return next question or result
POST /v1/quiz/elaborate   → submit elaboration for low confidence, re-score
POST /v1/quiz/followup    → post-results Q&A question, return Gemini answer
POST /v1/recommendations  → get VARK recommendations
POST /v1/process_quiz     → legacy single-turn endpoint
GET  /v1/debug            → health check
```
 
Rules:
- Use FastAPI with CORS middleware allowing all origins
- Store quiz session state in a module-level dict `QUIZ_SESSIONS = {}`
- On Railway: load `GOOGLE_APPLICATION_CREDENTIALS_JSON` env var, write to temp file, set `GOOGLE_APPLICATION_CREDENTIALS`
- `/v1/quiz/start` → generate UUID, initialize session state, return first question
- `/v1/quiz/answer` → append answer, increment index; if < 5 questions return next; if all answered call `process_quiz_input` and return result
- `/v1/quiz/elaborate` → append elaboration to session answers, re-call `process_quiz_input` with combined input
- `/v1/quiz/followup` → call `answer_followup` with session's dominant and scores
- Return 404 if session not found, 503 if dependencies missing, 500 on unexpected error
---
 
## Guardrail Reminders
 
Add these to any prompt if agent output is incorrect:
 
```
- "Do not hardcode any API keys, credentials, or project IDs."
- "Return ONLY the exact status strings specified. No extras."
- "Use exact key names: visual, auditory, reading, kinesthetic."
- "Use vertexai.GenerativeModel, NOT google.generativeai (deprecated)."
- "The mock patch target is src.engine.engine._get_client — ensure _get_client() returns the model directly."
- "MOCK_SCORES must include 'confidence': 85 for tests to pass the confidence threshold."
- "SESSION_STORE must be cleared between tests using an autouse fixture."
- "Import save_quiz_progress at the TOP of engine.py so the patch target src.engine.engine.save_quiz_progress is predictable."
- "run_session and run_quiz must accept process_fn as a parameter — never call process_quiz_input directly."
