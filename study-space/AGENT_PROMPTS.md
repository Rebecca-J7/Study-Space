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