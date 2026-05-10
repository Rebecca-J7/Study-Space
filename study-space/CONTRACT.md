# Study Space — API Contract

## save_quiz_progress(session_id: str, scores: dict) -> dict
- Required score keys: "visual", "auditory", "reading", "kinesthetic"
- Success:  {"status": "success", "id": "<session_id>"}
- Duplicate: {"status": "exists", "message": "Session already recorded."}
- Missing fields: {"status": "error", "message": "Missing required score fields."}

## get_recommendations(vark_result: dict) -> dict
- Required keys: "dominant", "strategies" (list), "tools" (list)
- Success: {"status": "success", "data": {"dominant": "Visual", "strategies": [...], "tools": [...]}}
- Tied: {"status": "tied", "data": {"tied_styles": [...], "strategies": [...]}}
- Failure: {"status": "error", "message": "Could not generate recommendations."}

## send_quiz_response(user_answer: str, question_index: int) -> dict
- Success: {"status": "success", "data": {"next_question": "...", "progress": 3}}
- Empty input: {"status": "empty_input", "message": "Please type an answer to continue."}

## clear_session(session_id: str) -> dict
- Success: {"status": "success", "message": "Session cleared."}
- Not found: {"status": "not_found", "message": "No active session found to reset."}