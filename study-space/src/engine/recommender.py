import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]

HARDCODED_TIPS = {
    "Visual": {
        "strategies": [
            "Use mind maps and diagrams to organize information",
            "Color-code your notes by topic or importance",
            "Watch video tutorials before reading textbooks",
            "Create flowcharts to map out processes",
            "Use flashcards with images and diagrams"
        ],
        "tools": ["Notion", "Canva", "YouTube", "MindMeister", "Anki"]
    },
    "Auditory": {
        "strategies": [
            "Record lectures and listen back while commuting",
            "Read your notes aloud when reviewing",
            "Join or form study groups for discussion",
            "Use text-to-speech tools for reading material",
            "Explain concepts out loud to yourself"
        ],
        "tools": ["Spotify Podcasts", "Voice Memos", "Otter.ai", "YouTube", "Google Podcasts"]
    },
    "Reading": {
        "strategies": [
            "Rewrite notes in your own words after class",
            "Make detailed outlines before studying",
            "Summarize each chapter in bullet points",
            "Read multiple sources on the same topic",
            "Keep a study journal to track progress"
        ],
        "tools": ["Notion", "Google Docs", "Anki", "Readwise", "Kindle"]
    },
    "Kinesthetic": {
        "strategies": [
            "Use hands-on practice and real-world examples",
            "Take frequent breaks and study in short bursts",
            "Teach concepts to others to reinforce learning",
            "Use physical flashcards you can move and sort",
            "Apply concepts to projects as you learn them"
        ],
        "tools": ["Anki", "Quizlet", "Khan Academy", "Codecademy", "Duolingo"]
    }
}


def _get_client():
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_recommendations(vark_result: dict) -> dict:
    required = ["dominant", "visual", "auditory", "reading", "kinesthetic"]
    for key in required:
        if key not in vark_result:
            return {"status": "error", "message": "Could not generate recommendations."}

    dominant = vark_result["dominant"]
    scores = {k: vark_result[k] for k in REQUIRED_KEYS}

    # Get hardcoded tips as base
    hardcoded = HARDCODED_TIPS.get(dominant, HARDCODED_TIPS["Visual"])

    # Check for tied styles
    max_score = max(scores.values())
    tied_styles = [k.capitalize() for k, v in scores.items() if v == max_score]

    try:
        client = _get_client()
        prompt = f"""
A student completed a VARK learning style quiz with these results:
Visual: {scores['visual']}%, Auditory: {scores['auditory']}%, 
Reading: {scores['reading']}%, Kinesthetic: {scores['kinesthetic']}%
Dominant style: {dominant}

Give 3 highly specific, personalized study tips for this exact score profile.
Keep each tip to one sentence. Do not use generic advice.
Format as a plain numbered list, no markdown, no headers.
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        gemini_tips = response.text.strip().split("\n")
        gemini_tips = [t.strip() for t in gemini_tips if t.strip()]

    except Exception:
        gemini_tips = []

    if len(tied_styles) > 1:
        return {
            "status": "tied",
            "data": {
                "tied_styles": tied_styles,
                "strategies": hardcoded["strategies"],
                "tools": hardcoded["tools"],
                "personalized_tips": gemini_tips
            }
        }

    return {
        "status": "success",
        "data": {
            "dominant": dominant,
            "strategies": hardcoded["strategies"],
            "tools": hardcoded["tools"],
            "personalized_tips": gemini_tips
        }
    }