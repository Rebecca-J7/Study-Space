# Study Space — Gemini Agent Prompts

## Prompt A: Storage Handler
Create `src/storage/storage_handler.py` for a study style quiz app called Study Space.

Implement:
    save_quiz_progress(session_id: str, scores: dict) -> dict

Rules:
- Use gspread and authenticate via service_account.json (no hardcoded secrets)
- Required score keys: "visual", "auditory", "reading", "kinesthetic"
- Missing key → return {"status": "error", "message": "Missing required score fields."}
- Duplicate session_id → return {"status": "exists", "message": "Session already recorded."}
- Success → return {"status": "success", "id": "<session_id>"}
- Return ONLY: "success", "exists", "error" — no other status values

## Prompt B: Engine — Recommendations
Create `src/engine/recommender.py` for Study Space.

Implement:
    get_recommendations(vark_result: dict) -> dict

Rules:
- Call the Gemini API using google-genai, load API key from .env (no hardcoded secrets)
- Required input keys: "dominant", scores for all four VARK styles
- Return tailored strategies and tools for the dominant style
- If two styles are tied, return both
- Success → {"status": "success", "data": {"dominant": "...", "strategies": [...], "tools": [...]}}
- Tied → {"status": "tied", "data": {"tied_styles": [...], "strategies": [...]}}
- Failure → {"status": "error", "message": "Could not generate recommendations."}
- Return ONLY: "success", "tied", "error"

## Guardrail Reminders (add to any prompt if output is wrong)
- "Do not hardcode any API keys or credentials."
- "Return ONLY the exact status strings specified. No extras."
- "Use exact key names: visual, auditory, reading, kinesthetic."
- "Authenticate using service_account.json loaded at runtime."

## Prompt C: Engine — Full Chain (Tool Use + Reflection)
Create `src/engine/engine.py` for a study style quiz app called Study Space.

CRITICAL: Use ONLY `from google import genai` — do NOT use `google.generativeai` (it is deprecated).

Implement these three functions:

1. extract_vark_scores(user_input: str) -> dict
2. reflect_on_scores(extracted: dict) -> dict
3. process_quiz_input(session_id: str, user_input: str) -> dict

Rules:
- Import at the TOP of the file:
    from google import genai
    from src.storage.storage_handler import save_quiz_progress
- Load GEMINI_API_KEY from .env using python-dotenv
- Initialize client lazily inside a helper: def _get_client(): return genai.Client(api_key=os.environ["GEMINI_API_KEY"])
- REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]

extract_vark_scores (Tool Use pattern):
- Call Gemini using: client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
- Prompt Gemini to return ONLY valid JSON with keys: visual, auditory, reading, kinesthetic as integers summing to 100
- Strip markdown fences (```json) before parsing
- Return {"status": "success", "data": {"visual": ..., "auditory": ..., "reading": ..., "kinesthetic": ...}}
- On any failure return {"status": "error", "message": "Could not extract scores."}

reflect_on_scores (Reflection pattern):
- No Gemini call — check locally whether all REQUIRED_KEYS are present
- Return {"complete": True, "missing": []} if all keys present
- Return {"complete": False, "missing": ["key1", ...]} if any keys missing

process_quiz_input (Full chain):
- Call extract_vark_scores(user_input)
- If extraction fails → return {"status": "error", "message": "Could not extract scores."}
- Call reflect_on_scores on the extracted data
- If incomplete → return {"status": "incomplete", "missing": [...]} and do NOT call save_quiz_progress
- If complete → call save_quiz_progress(session_id, extracted data) and return its result
- Return ONLY: "success", "exists", "error", "incomplete"
