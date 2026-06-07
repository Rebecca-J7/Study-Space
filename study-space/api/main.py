from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv
import os
import tempfile

_creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if _creds_json:
    _tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    _tmp.write(_creds_json)
    _tmp.close()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _tmp.name

# Ensure package imports work when running from the study-space folder
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

load_dotenv()

local_agent = None


def _import_engine():
    global local_agent
    try:
        from src.engine.engine import process_quiz_input
        from src.engine.recommender import get_recommendations
        import agent as local_agent_mod
        local_agent = local_agent_mod
        return process_quiz_input, get_recommendations
    except Exception as e:
        # Return None to indicate missing optional dependencies
        return None, None


class QuizRequest(BaseModel):
    session_id: str | None = None
    input: str


class VarkRequest(BaseModel):
    vark_result: dict


class AgentRequest(BaseModel):
    prompt: str


app = FastAPI(title="Study Space API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: allow overriding the sheet/service path via env
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")



@app.post("/v1/process_quiz")
def process_quiz(req: QuizRequest):
    process_quiz_input, _ = _import_engine()
    if process_quiz_input is None:
        raise HTTPException(status_code=503, detail="Backend AI dependencies not installed. See study-space/README_INTEGRATION.md")
    session_id = req.session_id or str(uuid.uuid4())
    try:
        result = process_quiz_input(session_id, req.input)
        return {"session_id": session_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/recommendations")
def recommendations(req: VarkRequest):
    _, get_recommendations = _import_engine()
    if get_recommendations is None:
        raise HTTPException(status_code=503, detail="Backend AI dependencies not installed. See study-space/README_INTEGRATION.md")
    try:
        return get_recommendations(req.vark_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/agent")
def agent(req: AgentRequest):
    # Ensure agent module is available
    process_quiz_input, get_recommendations = _import_engine()
    if local_agent is None:
        raise HTTPException(status_code=503, detail="Agent dependencies not installed. See study-space/README_INTEGRATION.md")
    try:
        text = local_agent.run_agent(req.prompt)
        return {"response": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/debug")
def debug():
    try:
        from src.engine.engine import extract_vark_scores
        result = extract_vark_scores("I love watching videos and diagrams")
        return {"result": result}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    
# In-memory session store for quiz state
QUIZ_SESSIONS = {}

QUIZ_QUESTIONS = [
    "Q1: When learning something new, do you prefer watching a video/diagram or reading a written explanation?",
    "Q2: When you need to remember something, do you write it down, say it out loud, or do something physical?",
    "Q3: When solving a problem, do you sketch it out, talk it through, write steps, or just try it hands-on?",
    "Q4: In class, do you learn best from slides/visuals, lectures, handouts, or lab/practice activities?",
    "Q5: When reviewing for an exam, do you use diagrams, recordings, notes/summaries, or practice problems?"
]


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


class FollowupRequest(BaseModel):
    session_id: str
    question: str


@app.post("/v1/quiz/start")
def quiz_start():
    """Start a new quiz session and return the first question."""
    session_id = str(uuid.uuid4())
    QUIZ_SESSIONS[session_id] = {
        "answers": [],
        "question_index": 0,
        "complete": False,
        "result": None
    }
    return {
        "session_id": session_id,
        "question": QUIZ_QUESTIONS[0],
        "question_number": 1,
        "total_questions": len(QUIZ_QUESTIONS)
    }


@app.post("/v1/quiz/answer")
def quiz_answer(req: AnswerRequest):
    """Submit an answer to the current question."""
    session = QUIZ_SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Please start a new quiz.")

    # Save answer
    session["answers"].append(req.answer)
    session["question_index"] += 1

    # If more questions remain return the next one
    if session["question_index"] < len(QUIZ_QUESTIONS):
        return {
            "session_id": req.session_id,
            "question": QUIZ_QUESTIONS[session["question_index"]],
            "question_number": session["question_index"] + 1,
            "total_questions": len(QUIZ_QUESTIONS),
            "status": "in_progress"
        }

    # All questions answered — score them
    process_quiz_input, _ = _import_engine()
    if process_quiz_input is None:
        raise HTTPException(status_code=503, detail="Backend AI dependencies not installed.")

    combined = " ".join(session["answers"])
    result = process_quiz_input(req.session_id, combined)
    session["result"] = result
    session["complete"] = result.get("status") != "low_confidence"

    return {
        "session_id": req.session_id,
        "status": result.get("status"),
        "result": result
    }


@app.post("/v1/quiz/elaborate")
def quiz_elaborate(req: AnswerRequest):
    """Submit elaboration when confidence is low."""
    session = QUIZ_SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    process_quiz_input, _ = _import_engine()
    if process_quiz_input is None:
        raise HTTPException(status_code=503, detail="Backend AI dependencies not installed.")

    # Add elaboration to existing answers and re-score
    session["answers"].append(req.answer)
    combined = " ".join(session["answers"])
    result = process_quiz_input(req.session_id, combined)
    session["result"] = result
    session["complete"] = result.get("status") != "low_confidence"

    return {
        "session_id": req.session_id,
        "status": result.get("status"),
        "result": result
    }


@app.post("/v1/quiz/followup")
def quiz_followup(req: FollowupRequest):
    """Ask a follow-up question after results are shown."""
    session = QUIZ_SESSIONS.get(req.session_id)
    if not session or not session.get("result"):
        raise HTTPException(status_code=404, detail="No completed session found.")

    try:
        from src.engine.engine import answer_followup
        result = session["result"]
        dominant = result.get("dominant", "Visual")
        scores = result.get("scores", {})
        answer = answer_followup(req.question, dominant, scores)
        return {
            "session_id": req.session_id,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port)
