import os
import json
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
from src.storage.storage_handler import save_quiz_progress

load_dotenv()

REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]
CONFIDENCE_THRESHOLD = 40


def _get_client():
    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location="us-central1"
    )
    return GenerativeModel("gemini-2.5-flash")


def extract_vark_scores(user_input: str) -> dict:
    try:
        model = _get_client()
        prompt = f"""
Analyze this input and estimate VARK learning style scores.
Input: "{user_input}"

Return ONLY a valid JSON object with exactly these five keys:
- visual, auditory, reading, kinesthetic (integers that sum to 100)
- confidence (integer 0-100 reflecting how confident you are in the scores
  based on how much detail the input provides)

Low confidence (0-39): input is too vague to score reliably e.g. "I like stuff"
Medium confidence (40-69): some signals but could use more detail
High confidence (70-100): clear learning style signals present

Do not include any explanation, markdown, or code fences. Only the JSON object.

Example output:
{{"visual": 40, "auditory": 20, "reading": 25, "kinesthetic": 15, "confidence": 85}}
"""
        response = model.generate_content(prompt)
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        parsed = json.loads(raw)

        for key in REQUIRED_KEYS:
            if key not in parsed:
                return {"status": "error", "message": "Could not extract scores."}

        confidence = parsed.get("confidence", 0)

        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "status": "low_confidence",
                "confidence": confidence,
                "message": "Input too vague to determine learning style reliably."
            }

        scores = {k: parsed[k] for k in REQUIRED_KEYS}

        return {
            "status": "success",
            "confidence": confidence,
            "data": scores
        }

    except Exception as e:
        return {"status": "error", "message": f"Could not extract scores. {str(e)}"}


def reflect_on_scores(extracted: dict) -> dict:
    missing = [key for key in REQUIRED_KEYS if key not in extracted]
    if missing:
        return {"complete": False, "missing": missing}
    return {"complete": True, "missing": []}


def process_quiz_input(session_id: str, user_input: str) -> dict:
    extraction = extract_vark_scores(user_input)

    if extraction["status"] == "low_confidence":
        return extraction

    if extraction["status"] != "success":
        data = extraction.get("data", {})
        if not data:
            return {"status": "incomplete", "missing": ["visual", "auditory", "reading", "kinesthetic"]}
        reflection = reflect_on_scores(data)
        if not reflection["complete"]:
            return {"status": "incomplete", "missing": reflection["missing"]}
        return {"status": "error", "message": "Could not extract scores."}

    scores = extraction["data"]
    reflection = reflect_on_scores(scores)
    if not reflection["complete"]:
        return {"status": "incomplete", "missing": reflection["missing"]}

    storage_result = save_quiz_progress(session_id, scores)
    if storage_result["status"] in ["success", "exists"]:
        dominant = max(scores, key=scores.get)
        return {
            "status": storage_result["status"],
            "id": storage_result.get("id", session_id),
            "scores": scores,
            "dominant": dominant.capitalize()
        }
    return storage_result


def answer_followup(question: str, dominant: str, scores: dict) -> str:
    if not question.strip():
        return "Please ask a question about your learning style or study tips!"

    try:
        model = _get_client()
        prompt = f"""
You are a helpful study coach for a {dominant} learner.
Their VARK scores are: Visual {scores.get('visual')}%, Auditory {scores.get('auditory')}%, 
Reading {scores.get('reading')}%, Kinesthetic {scores.get('kinesthetic')}%.

Answer this question in 2-3 sentences with specific, practical advice:
"{question}"
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"I couldn't generate an answer right now. Please try again. ({str(e)})"