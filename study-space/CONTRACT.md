### Functionality 1: VARK Learning Style Quiz
- `interface` responsibilities: display quiz questions one at a time conversationally, collect user responses, show progress
- `engine` responsibilities: Gemini interprets each answer, tracks scoring across VARK categories, determines dominant style
- `storage` responsibilities: temporarily store quiz responses and running scores for session duration

### `interface -> engine`
- `send_quiz_response(user_answer: str, question_index: int) -> response_payload`
- Success: `{"status": "success", "data": {"next_question": "Do you prefer diagrams or written instructions?", "progress": 3}}`
- Failure: `{"status": "empty_input", "message": "Please type an answer to continue."}`

### `engine -> storage`
- `save_quiz_progress(session_id: str, scores: vark_scores) -> response_payload`
- Success: `{"status": "success", "data": {"visual": 40, "auditory": 20, "reading": 15, "kinesthetic": 25}}`
- Failure: `{"status": "error", "message": "Could not save session progress."}`

### Functionality 2: Personalized Study Method Recommendations

- `interface` display final VARK breakdown with a visual profile card and a list of recommended study strategies and tools
- `engine` takes VARK scores and generates tailored recommendations via Gemini prompt
- `storage` optionally save recommendations to session so user can revisit without re-running

### `interface -> engine`
- `get_recommendations(vark_result: vark_scores) -> response_payload`
- Success: `{"status": "success", "data": {"dominant": "Visual", "strategies": ["Use mind maps", "Color-code notes", "Watch video summaries"], "tools": ["Canva", "YouTube", "Notion"]}}`
- Failure: `{"status": "tied", "message": "Multiple styles tied.", "data": {"tied_styles": ["Visual", "Kinesthetic"], "strategies": [...]}}`

### `engine -> storage`
- `save_recommendations(session_id: str, recommendations: recommendation_record) -> response_payload`
- Success: `{"status": "success", "id": "rec_session_456"}`
- Failure: `{"status": "error", "message": "Could not store recommendations."}`

### Functionality 3: Quiz Retake & Profile Reset

- `interface` show retake button after results, display confirmation dialog before clearing, restart quiz on confirm
- `engine` clear current VARK scores and recommendations, reinitialize quiz state
- `storage` delete or overwrite existing session record for the user

### `interface -> engine`
- `request_retake(session_id: str) -> response_payload`
- Success: `{"status": "confirmed", "message": "Your profile has been reset. Let's start fresh!"}`
- Failure: `{"status": "cancelled", "message": "Retake cancelled. Your current results are still saved."}`

### `engine -> storage`
- `clear_session(session_id: str) -> response_payload`
- Success: `{"status": "success", "message": "Session cleared.", "id": "session_789"}`
- Failure: `{"status": "not_found", "message": "No active session found to reset."}`

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
