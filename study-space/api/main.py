from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv
import os

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("study-space.api.main:app", host="127.0.0.1", port=8001, reload=True)
